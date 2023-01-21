from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import recruiter_schema, schemas


class PostBase(BaseModel):
    title: str
    description: str
    salaryRange: str
    communicationLang: str
    joiningPeriod: str
    workLocation: str
    officeLocation: str
    jobType: str
    jobLevel: str
    jobStage: str
    jobDomain: str
    educationLevel: str
    experienceLevel: str
    numberOfPositionOpen: str
    rolesAndResponsibilities: str
    reportingTo: str
    screeningRounds: str
    backgroundVerificationApplicable: bool
    benifitsProvided: str


class PostCreate(PostBase):
    pass


class PostResponse(PostBase):
    id: int
    published: bool
    createdAt: datetime
    postTimePeriod: datetime
    owner_id: int
    recruiterId: int
    owner: schemas.UserResponse
    recruiter: recruiter_schema.RecruiterResponse

    class Config:
        orm_mode = True


class PostOut(BaseModel):
    Post: PostResponse
    reviews: int
    # RecruiterProfile: recruiter_schema.RecruiterResponse

    class Config:
        orm_mode = True
