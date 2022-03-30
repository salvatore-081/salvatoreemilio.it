from typing import Optional, List
from pydantic import BaseModel


class User(BaseModel):
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    phoneNumber: Optional[str] = None
    location: Optional[str] = None
    profilePicture: Optional[bytes] = None


class UserListItem(BaseModel):
    email: str
    name: Optional[str] = None
    surname: Optional[str] = None
    profilePicture: Optional[bytes] = None


class UserList(BaseModel):
    userList: List[UserListItem]


class UpdateUserInputPayload(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phoneNumber: Optional[str] = None
    location: Optional[str] = None
    profilePicture: Optional[bytes] = None
