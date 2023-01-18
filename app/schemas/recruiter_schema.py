from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class CreateRecruiter(BaseModel):
    jobTitle: str
    companyName: str
    industry: str
    noticePeriod: str
    websiteUrl: Optional[str] = None
    linkedInUrl: Optional[str] = None
    otherUrl: Optional[str] = None
    profilePicUrl: Optional[str] = None
    bannerPicUrl: Optional[str] = None
    hiringRoleTitle: Optional[str] = None
    hiringRoleDescription: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateRecruiter(BaseModel):
    jobTitle: Optional[str]
    companyName: Optional[str]
    industry: Optional[str]
    noticePeriod: Optional[str]
    websiteUrl: Optional[str]
    linkedInUrl: Optional[str]
    otherUrl: Optional[str]
    profilePicUrl: Optional[str]
    bannerPicUrl: Optional[str]
    hiringRoleTitle: Optional[str]
    hiringRoleDescription: Optional[str]

    class Config:
        orm_mode = True


class RecruiterResponse(BaseModel):
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
