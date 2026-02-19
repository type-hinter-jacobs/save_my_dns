from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI, Depends, HTTPException, status
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.api.schemas import BlockedDomainCreate, BlockedDomainResponse, BlockedDomainUpdate
from src.api.repo_provider import get_repo
from src.repository.exceptions import DomainAlreadyBlocked, DomainNotFound
from src.models import BlockedDomain
from src.api.auth import require_admin_key


app = FastAPI(title="Save My DNS - Admin API")

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