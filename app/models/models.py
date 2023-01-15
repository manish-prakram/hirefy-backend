from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class RecruiterProfile(Base):
    __tablename__ = 'recruiter_profile'
    id = Column(Integer, primary_key=True, nullable=False)
    jobTitle = Column(String)
    companyName = Column(String)
    industry = Column(String)
    noticePeriod = Column(String)
    websiteUrl = Column(String)
    linkedInUrl = Column(String)
    otherUrl = Column(String)
    profilePicUrl = Column(String)
    bannerPicUrl = Column(String)
    hiringRoleTitle = Column(String)
    hiringRoleDescription = Column(String)
    lastLogin = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        server_default=text('now()'), nullable=False)
    firstName = Column(String)
    lastName = Column(String)
    dateOfBirth = Column(String)
    age = Column(String)
    gender = Column(String)
    profilePicUrl = Column(String)
    phone_number = Column(String)
    phoneVerified = Column(Boolean, server_default='FALSE', nullable=False)
    emailVerified = Column(Boolean, server_default='FALSE', nullable=False)
    isVerified = Column(Boolean, server_default='FALSE', nullable=False)
    isBlocked = Column(Boolean, server_default='FALSE', nullable=False)
    otpCode = Column(String)
    deviceType = Column(String)
    lastLogin = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    workEmail = Column(String)
    profileType = Column(Integer)
    requisitionId = Column(Integer)
    profileId = Column(Integer)


class Review(Base):
    __tablename__ = 'reviews'

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    ratings = Column(Integer)
    reviews = Column(String)
