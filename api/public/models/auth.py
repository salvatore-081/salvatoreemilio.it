from typing import Optional
from pydantic import BaseModel


class Login(BaseModel):
    username: str
    password: str
    totp: Optional[str]
