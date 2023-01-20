from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import recruiter_schema


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True  # Use default value for optional parameter
    # rating: Optional[int] = None  # USe Optional import from typing


class PostCreate(PostBase):
    pass


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


class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    reviews: int
    # RecruiterProfile: recruiter_schema.RecruiterResponse

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


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: str
    dir: conint(le=1)
