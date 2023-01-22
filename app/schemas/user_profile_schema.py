from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import schemas, technical_skills_schema


class CreateUserProfile(BaseModel):
    currentJobTitle: str
    totalExperience: str
    currentCompany: str
    currentIndustry: str
    noticePeriod: str
    negotiableNoticePeriod: bool
    publicCompetitionLink: Optional[str] = None
    publicCompetitionScores: Optional[str] = None
    websiteUrl: Optional[str] = None
    linkedInUrl: Optional[str] = None
    githubUrl: Optional[str] = None
    twitterUrl: Optional[str] = None
    mediumUrl: Optional[str] = None
    behanceUrl: Optional[str] = None
    otherUrl: Optional[str] = None
    fixedPay: str
    incentives: Optional[str] = None
    bonus: Optional[str] = None
    currency: Optional[str] = None
    expectedCtc: str
    negotiableExpectedCtc: bool
    bechelorsDegree: Optional[str] = None
    mastersDegree: Optional[str] = None
    phd: Optional[str] = None
    deplomaCourse: Optional[str] = None

    class Config:
        orm_mode = True


class UpdateUserProfile(BaseModel):
    currentJobTitle: Optional[str]
    totalExperience: Optional[str]
    currentCompany: Optional[str]
    currentIndustry: Optional[str]
    noticePeriod: Optional[str]
    negotiableNoticePeriod: Optional[bool]
    publicCompetitionLink: Optional[str]
    publicCompetitionScores: Optional[str]
    websiteUrl: Optional[str]
    linkedInUrl: Optional[str]
    githubUrl: Optional[str]
    twitterUrl: Optional[str]
    mediumUrl: Optional[str]
    behanceUrl: Optional[str]
    otherUrl: Optional[str]
    fixedPay: Optional[str]
    incentives: Optional[str]
    bonus: Optional[str]
    currency: Optional[str]
    expectedCtc: Optional[str]
    negotiableExpectedCtc: Optional[bool]
    bechelorsDegree: Optional[str]
    mastersDegree: Optional[str]
    phd: Optional[str]
    deplomaCourse: Optional[str]

    class Config:
        orm_mode = True



class ResponseUserProfile(BaseModel):
    currentJobTitle: str
    totalExperience: str
    currentCompany: str
    currentIndustry: str
    noticePeriod: str
    negotiableNoticePeriod: bool
    publicCompetitionLink: str = None
    publicCompetitionScores: str = None
    websiteUrl: str = None
    linkedInUrl: str = None
    githubUrl: str = None
    twitterUrl: str = None
    mediumUrl: str = None
    behanceUrl: str = None
    otherUrl: str = None
    fixedPay: str
    incentives: str = None
    bonus: str = None
    currency: Optional[str] = None
    expectedCtc: str = None
    negotiableExpectedCtc: bool
    bechelorsDegree: str = None
    mastersDegree: str = None
    phd: str = None
    deplomaCourse: str = None
    owner: schemas.UserResponse
    # techSkills: TechnicalSkillsResponse

    class Config:
        orm_mode = True
