from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ..schemas import recruiter_schema, schemas


class PostBase(BaseModel):
    title: Optional[str]
    description: Optional[str]
    salaryRange: Optional[str]
    communicationLang: Optional[str]
    joiningPeriod: Optional[str]
    workLocation: Optional[str]
    officeLocation: Optional[str]
    jobType: Optional[str]
    jobLevel: Optional[str]
    jobStage: Optional[str]
    jobDomain: Optional[str]
    educationLevel: Optional[str]
    experienceLevel: Optional[str]
    numberOfPositionOpen: Optional[str]
    rolesAndResponsibilities: Optional[str]
    reportingTo: Optional[str]
    screeningRounds: Optional[str]
    backgroundVerificationApplicable: bool
    benifitsProvided: Optional[str]


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
