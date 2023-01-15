from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class CreateRecruiter(BaseModel):
    jobTitle: str
    companyName: str
    industry: str
    noticePeriod: str
    websiteUrl: str = None
    linkedInUrl: str = None
    otherUrl: str = None
    profilePicUrl: str = None
    bannerPicUrl: str = None
    hiringRoleTitle: str = None
    hiringRoleDescription: str = None

    class Config:
        orm_mode = True


class RecruiterResponse(BaseModel):
    id: int
    jobTitle: str
    companyName: str
    industry: str
    noticePeriod: str
    websiteUrl: str = None
    linkedInUrl: str = None
    otherUrl: str = None
    profilePicUrl: str = None
    bannerPicUrl: str = None
    hiringRoleTitle: str = None
    hiringRoleDescription: str = None
    owner_id: str
    lastLogin: datetime

    class Config:
        orm_mode = True
