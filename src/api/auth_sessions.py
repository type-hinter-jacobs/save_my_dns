import os
from fastapi import Request, status
from fastapi.responses import RedirectResponse


def login(request: Request, submitted_key: str) -> bool:
    if submitted_key == os.environ.get("SAVE_MY_DNS_ADMIN_KEY"):
        request.session["is_admin"] = True
        return True
    request.session["is_admin"] = False
    return False

def logout(request: Request) -> None:
    request.session.clear()

def require_admin_session(request: Request):
    if not request.session.get("is_admin", False):
        return RedirectResponse("/login", status_code=status.HTTP_303_SEE_OTHER)



