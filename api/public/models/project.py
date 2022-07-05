from typing import List, Optional
from pydantic import BaseModel

class Link(BaseModel):
    name: str
    url: str

class Project(BaseModel):
    id: str
    email: str
    title: str
    description: str
    image: bytes
    tags: List[str]
    links: List[Link]
    index: int

class Projects(BaseModel): 
    projects: Optional[List[Project]]

class AddProjectInput(BaseModel):
    email: str
    title: str
    description: str
    image: bytes
    tags: List[str]
    links: List[Link]

class UpdateProjectInputPayload(BaseModel):
    title: Optional[str]
    description: Optional[str]
    image: Optional[bytes]
    tags: Optional[List[str]]
    links: Optional[List[Link]]
    index: Optional[int]

class DeleteProjectOutput(BaseModel):
    id: str