from typing import Optional
from pydantic import BaseModel


class LoginInput(BaseModel):
    username: str
    password: str
    totp: Optional[str]


class LoginResponse(BaseModel):
    access_token: str
    expires_in: int
    refresh_expires_in: int
    refresh_token: str
    token_type: str
    session_state: str
    scope: str
