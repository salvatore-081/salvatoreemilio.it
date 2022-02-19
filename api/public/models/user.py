from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    phoneNumber: Optional[str] = None
    currentLocation: Optional[str] = None
