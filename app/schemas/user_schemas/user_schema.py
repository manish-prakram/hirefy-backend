from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from ...schemas import schemas


class UpdateUser(BaseModel):
    firstName: Optional[str]
    middleName: Optional[str]
    lastName: Optional[str]
    email: Optional[str]
    workEmail: Optional[str]
    gender: Optional[str]
    dateOfBirth: Optional[str]
    age: Optional[str]
    phone_number: Optional[str]
    currentLocation: Optional[str]
    latitude: Optional[str]
    longitude: Optional[str]
    profilePicUrl: Optional[str]
    coverPicUrl: Optional[str]
    profileType: Optional[int]
    phoneVerified: Optional[bool]
    emailVerified: Optional[bool]
    requisitionId: Optional[int]
    profileId: Optional[int]
    isVerified: Optional[bool]
    isBlocked: Optional[bool]
    isLoggedIn: Optional[int]
    otpCode: Optional[str]
    deviceType: Optional[str]
    appVersion: Optional[str]


class UserResponse(BaseModel):
    id: int
    firstName: str = None
    middleName: str = None
    lastName: str = None
    email: str = None
    workEmail: str = None
    gender: str = None
    dateOfBirth: str = None
    age: str = None
    phone_number: str = None
    currentLocation: str = None
    latitude: str = None
    longitude: str = None
    profilePicUrl: str = None
    coverPicUrl: str = None
    profileType: int = None
    phoneVerified: bool = None
    emailVerified: bool = None
    requisitionId: int = None
    profileId: int = None
    isVerified: bool = None
    isBlocked: bool = None
    isLoggedIn: int = None
    otpCode: str = None
    deviceType: str = None
    appVersion: str = None
    lastLogin: datetime = None
    created_at: datetime = None

    class Config:
        orm_mode = True
