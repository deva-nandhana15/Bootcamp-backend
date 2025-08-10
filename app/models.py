from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List, Any

# Auth
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: str = Field(..., alias="_id")
    name: str
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Section & Task payloads
class SectionCreate(BaseModel):
    name: str

class SectionOut(BaseModel):
    id: str
    name: str

class TaskCreate(BaseModel):
    title: str
    status: str
    section_id: str

class TaskOut(BaseModel):
    id: str
    title: str
    status: str
    section_id: Optional[str]
