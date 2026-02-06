from pydantic import BaseModel, Field


class BlockedDomainCreate(BaseModel):
    domain: str = Field(min_length=1)

class BlockedDomainResponse(BaseModel):
    domain: str = Field(min_length=1)
    enabled: bool

class BlockedDomainUpdate(BaseModel):
    enabled: bool


