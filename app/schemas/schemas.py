from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import recruiter_schema



class UserProfileType(BaseModel):
    profileType: str

    class Config:
        orm_mode = True


class UserResponse(BaseModel):
    
    email: EmailStr
    phone_number: str = None
    firstName: str = None
    lastName: str = None
    created_at: datetime

    class Config:
        orm_mode = True



class CreateUser(BaseModel):
    email: EmailStr
    password: str
    phone_number: str = None
    # otpCode: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    email: str
    access_token: str
    token_type: str
    emailVerified: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)
