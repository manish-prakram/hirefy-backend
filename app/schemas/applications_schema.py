from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from app.schemas.posts_schema import PostResponse
from app.schemas.user_schemas.user_schema import UserResponse


class CreateApplication(BaseModel):
    postId: int
    status: int


class UpdateApplicationStatus(BaseModel):
    id: int
    status: int

    class Config:
        orm_mode = True


class ApplicationsResponse(BaseModel):
    id: int
    userId: int
    postId: int
    status: int
    owner_id: int
    recruiterId: int
    createdAt: datetime
    updatedAt: datetime

    class Config:
        orm_mode = True


class CandidateAppliPostResponse(BaseModel):
    Applications: ApplicationsResponse
    Post: PostResponse

    class Config:
        orm_mode = True


class ApplicationUserDetailsRes(BaseModel):
    Applications: ApplicationsResponse
    User: UserResponse

    class Config:
        orm_mode = True
