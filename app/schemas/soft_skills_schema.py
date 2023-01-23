from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import schemas


class CreateSoftSkill(BaseModel):
    title: str
    experienceLevel: str
    experience: str


class UpdateSoftSkill(BaseModel):
    title: Optional[str]
    experienceLevel: Optional[str]
    experience: Optional[str]


class SoftSkillsResponse(BaseModel):
    id: str
    title: str
    experienceLevel: str
    experience: str
