from fastapi import Depends, HTTPException, status
from fastapi.security import APIKeyHeader
import os


api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def require_admin_key(api_key: str = Depends(api_key_header)):
    SAVE_MY_DNS_ADMIN_KEY = os.environ.get("SAVE_MY_DNS_ADMIN_KEY")
    if api_key is None:
        raise HTTPException(status_code=401, detail="API key not provided")
    elif api_key != SAVE_MY_DNS_ADMIN_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key provided")