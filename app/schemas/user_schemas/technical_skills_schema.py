from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ...schemas import schemas


class CreateTechnicalSkill(BaseModel):
    title: str
    experienceLevel: str
    experience: str


class UpdateTechnicalSkill(BaseModel):
    title: Optional[str]
    experienceLevel: Optional[str]
    experience: Optional[str]


class TechnicalSkillsResponse(BaseModel):
    id: str
    title: str
    experienceLevel: str
    experience: str
