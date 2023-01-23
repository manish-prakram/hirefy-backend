from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Education(Base):
    __tablename__ = 'education'

    id = Column(Integer, primary_key=True, nullable=False)
    userProfileId = Column(Integer, ForeignKey(
        "users_profile.id", ondelete="CASCADE"), nullable=False)
    course = Column(String)
    branch = Column(String)
    school = Column(String)
    startDate = Column(TIMESTAMP)
    endDate = Column(TIMESTAMP)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    owner = relationship("UserProfile")
