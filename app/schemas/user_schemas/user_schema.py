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
