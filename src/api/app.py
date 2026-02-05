from fastapi import FastAPI, Depends, HTTPException, status
from src.repository.denylist import SQLAlchemyDenylistRepository
from src.api.schemas import BlockedDomainCreate, BlockedDomainResponse
from src.api.repo_provider import get_repo
from src.repository.exceptions import DomainAlreadyBlocked
from src.models import BlockedDomain


app = FastAPI(title="Save My DNS - Admin API")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post("/blocked-domains", status_code=status.HTTP_201_CREATED, response_model=BlockedDomainResponse)
def add_blocked_domain(payload: BlockedDomainCreate, repo: SQLAlchemyDenylistRepository = Depends(get_repo)):
    normalised_domain = BlockedDomain.normalise_domain(payload.domain)
    try:
        repo.add(domain=normalised_domain)
        return {"domain": normalised_domain, "enabled": True}
    except DomainAlreadyBlocked:
        raise HTTPException(status_code=409, detail="Domain already blocked")


# python -m uvicorn src.api.app:app --reload --port 8000