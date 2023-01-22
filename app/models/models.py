from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    salaryRange = Column(String, nullable=False)
    communicationLang = Column(String)
    joiningPeriod = Column(String)
    workLocation = Column(String)
    officeLocation = Column(String)
    jobType = Column(String)
    jobLevel = Column(String)
    jobStage = Column(String)
    jobDomain = Column(String)
    educationLevel = Column(String)
    experienceLevel = Column(String)
    numberOfPositionOpen = Column(String)
    rolesAndResponsibilities = Column(String)
    reportingTo = Column(String)
    screeningRounds = Column(String)
    backgroundVerificationApplicable = Column(
        Boolean, server_default='TRUE', nullable=False)
    benifitsProvided = Column(String)
    published = Column(Boolean, server_default='TRUE', nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    postTimePeriod = Column(TIMESTAMP(timezone=True),
                            server_default=text('now()'), nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    recruiterId = Column(Integer, ForeignKey(
        "recruiter_profile.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    recruiter = relationship("RecruiterProfile")


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
    isCompanyAdmin = Column(Boolean, server_default='FALSE', nullable=False)
    company = relationship(
        "Company", back_populates="recruiter", uselist=False)


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


class UserProfile(Base):
    __tablename__ = 'users_profile'

    id = Column(Integer, primary_key=True, nullable=False)
    profileId = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    currentJobTitle = Column(String)
    totalExperience = Column(String)
    currentCompany = Column(String)
    currentIndustry = Column(String)
    noticePeriod = Column(String)
    negotiableNoticePeriod = Column(
        Boolean, server_default='TRUE', nullable=False)
    publicCompetitionLink = Column(String)
    publicCompetitionScores = Column(String)
    websiteUrl = Column(String)
    linkedInUrl = Column(String)
    githubUrl = Column(String)
    twitterUrl = Column(String)
    mediumUrl = Column(String)
    behanceUrl = Column(String)
    otherUrl = Column(String)
    fixedPay = Column(String)
    incentives = Column(String)
    bonus = Column(String)
    currency = Column(String)
    expectedCtc = Column(String)
    negotiableExpectedCtc = Column(
        Boolean, server_default='TRUE', nullable=False)
    bechelorsDegree = Column(String)
    mastersDegree = Column(String)
    phd = Column(String)
    deplomaCourse = Column(String)
    lastLogin = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    owner = relationship("User")
    techSkills = relationship(
        "TechnicalSkills", back_populates="owner", uselist=False)


class SoftSkills(Base):
    __tablename__ = 'soft_skills'
    id = Column(Integer, primary_key=True, nullable=False)
    userProfileId = Column(Integer, ForeignKey(
        "users_profile.id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    experience = Column(String)
    experienceLevel = Column(String)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    owner = relationship("UserProfile")


class TechnicalSkills(Base):
    __tablename__ = 'technical_skills'
    id = Column(Integer, primary_key=True, nullable=False)
    userProfileId = Column(Integer, ForeignKey(
        "users_profile.id", ondelete="CASCADE"), nullable=False)
    title = Column(String)
    experience = Column(String)
    experienceLevel = Column(String)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    owner = relationship(
        "UserProfile", back_populates="techSkills", uselist=False)


class Review(Base):
    __tablename__ = 'reviews'

    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)

    post_id = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    ratings = Column(Integer)
    reviews = Column(String)


class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, nullable=False)
    owner = relationship("User")
    recruiter = relationship("RecruiterProfile", back_populates="company")
    recruiterId = Column(Integer, ForeignKey(
        "recruiter_profile.id", ondelete="CASCADE"))
    adminId = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    companyName = Column(String)
    industry = Column(String)
    totalEmployees = Column(Integer)
    headquartered = Column(String)
    companyBio = Column(String)
    companyEmail = Column(String)
    profilePicUrl = Column(String)
    bannerPicUrl = Column(String)
    companyPics = Column(String)
    founders = Column(String)
    phone_number = Column(String)
    email = Column(String)
    companyGst = Column(String)
    websiteLink = Column(String)
    phoneVerified = Column(Boolean, server_default='FALSE', nullable=False)
    isVerified = Column(Boolean, server_default='FALSE', nullable=False)
    isBlocked = Column(Boolean, server_default='FALSE', nullable=False)
    lastLogin = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
