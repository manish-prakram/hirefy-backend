from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from app.schemas import schemas


class CreateExperience(BaseModel):
    title: str
    company: str
    jobType: str
    jobLocation: str
    jobDomain: str
    skills: str
    startDate: datetime
    endDate: datetime


class UpdateExperience(BaseModel):
    title: Optional[str]
    company: Optional[str]
    jobType: Optional[str]
    jobLocation: Optional[str]
    jobDomain: Optional[str]
    skills: Optional[str]
    startDate: Optional[datetime]
    endDate: Optional[datetime]
