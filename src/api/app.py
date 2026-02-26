from dotenv import load_dotenv
load_dotenv()
import os
from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.api.schemas import BlockedDomainCreate, BlockedDomainResponse, BlockedDomainUpdate
from src.api.repo_provider import get_repo
from src.repository.exceptions import DomainAlreadyBlocked, DomainNotFound
from src.models import BlockedDomain
from src.api.auth import require_admin_key
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware
from src.api.auth_sessions import login, logout, require_admin_session


app = FastAPI(title="Save My DNS - Admin API")

SESSION_SECRET = os.environ.get("SESSION_SECRET")

app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    same_site="lax",
    max_age=60 * 60 * 24 * 7
)

TEMPLATES_DIR = Path(__file__).resolve().parent / "templates"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/blocked-domains", status_code=status.HTTP_201_CREATED, response_model=BlockedDomainResponse, dependencies=[Depends(require_admin_key)])
def add_blocked_domain(payload: BlockedDomainCreate, repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(payload.domain)
    try:
        repo.add(domain=normalised_domain)
        return {"domain": normalised_domain, "enabled": True}
    except DomainAlreadyBlocked:
        raise HTTPException(status_code=409, detail="Domain already blocked")

@app.patch("/blocked-domains/{domain}", response_model=BlockedDomainResponse, dependencies=[Depends(require_admin_key)])
def update_blocked_domain_status(domain: str, payload: BlockedDomainUpdate, repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(domain)
    try:
        repo.set_enabled(domain=normalised_domain, enabled=payload.enabled)
        return {"domain": normalised_domain, "enabled": payload.enabled}
    except DomainNotFound:
        raise HTTPException(status_code=404, detail="Domain does not exist")

@app.delete("/blocked-domains/{domain}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(require_admin_key)])
def delete_blocked_domain(domain: str, repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(domain)
    try:
        repo.remove(domain=normalised_domain)
    except DomainNotFound:
        raise HTTPException(status_code=404, detail="Domain does not exist")

@app.get("/blocked-domains", response_model=list[BlockedDomainResponse])
def get_blocked_domains(repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    items = repo.list_all()
    return items

@app.get("/dashboard", dependencies=[Depends(require_admin_session)])
def dashboard(request: Request, repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    items = repo.list_all()
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse("dashboard.html", {"request": request, "items": items, "flash": flash})

@app.post("/dashboard/domains/{domain}/toggle", dependencies=[Depends(require_admin_session)])
def toggle_blocked_domain_status(domain: str, enabled: Annotated[str, Form()], repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(domain)
    enabled = enabled.strip().lower()
    if enabled == "true":
        toggle_bool = True
    elif enabled == "false":
        toggle_bool = False
    else:
        return status.HTTP_400_BAD_REQUEST
    repo.set_enabled(normalised_domain, toggle_bool)
    return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/dashboard/domains", dependencies=[Depends(require_admin_session)])
def add_domain(request: Request, domain: Annotated[str, Form()], repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(domain)
    try:
        repo.add(normalised_domain)
        request.session["flash"] = "Domain added successfully."
    except ValueError:
        request.session["flash"] = "Invalid domain."
    except DomainAlreadyBlocked:
        request.session["flash"] = "Domain already exists"
    return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login")
def login_page(request: Request):
    if request.session.get("is_admin"):
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse("login.html", {"request": request, "flash": flash})

@app.post("/login")
def login_submit(request: Request, admin_key: Annotated[str, Form()]):
    ok = login(request, admin_key)
    if ok:
        return RedirectResponse("/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    request.session["flash"] = "Invalid admin key."
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/logout", dependencies=[Depends(require_admin_session)])
def logout_user(request: Request):
    logout(request)
    return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)