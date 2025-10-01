from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from .models import UserRole, LeadStatus

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class LeadBase(BaseModel):
    client_name: str
    phone: str
    city_state: str
    observation: Optional[str] = None

class LeadCreate(LeadBase):
    vendedor_id: int

class LeadUpdate(BaseModel):
    status: LeadStatus
    observation: Optional[str] = None

class LeadResponse(LeadBase):
    id: int
    status: LeadStatus
    indicador_id: int
    vendedor_id: int
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
