from pydantic import BaseModel
from typing import Optional


class InternalServerError(BaseModel):
    detail: str = "Unexpected error"
    debug: Optional[str]


class NotFound(BaseModel):
    detail: str


class Conflict(BaseModel):
    detail: str

class Forbidden(BaseModel):
    detail: str = "Unauthorized"

class Unauthorized(BaseModel):
    detail: str = "Invalid credentials"


class BadRequest(BaseModel):
    detail: str
