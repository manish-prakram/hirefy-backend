from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from app.schemas import schemas


class CreateCertificate(BaseModel):
    title: str
    subtitle: str = None
    description: str
    organization: str
    licenceNumber: str
    url: str
    skills: str
    startDate: datetime
    endDate: datetime


class UpdateCertificate(BaseModel):
    title: Optional[str]
    subtitle: Optional[str]
    description: Optional[str]
    organization: Optional[str]
    licenceNumber: Optional[str]
    url: Optional[str]
    skills: Optional[str]
    startDate: Optional[datetime]
    endDate: Optional[datetime]
