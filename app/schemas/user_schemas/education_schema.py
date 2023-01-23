from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from app.schemas import schemas


class CreateEducation(BaseModel):
    course: str
    branch: str
    school: str
    startDate: datetime
    endDate: datetime


class UpdateEducation(BaseModel):
    course: Optional[str]
    branch: Optional[str]
    school: Optional[str]
    startDate: Optional[datetime]
    endDate: Optional[datetime]
