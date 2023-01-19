from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class CreateCompany(BaseModel):
    companyName: str
    industry: str
    totalEmployees: int
    headquartered: str
    companyBio: str
    companyEmail: str
    profilePicUrl: str
    bannerPicUrl: str
    companyPics: str
    founders: str
    phone_number: str
    email: str
    companyGst: str
    websiteLink: str

    class Config:
        orm_mode = True
