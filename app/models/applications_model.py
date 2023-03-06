from ..database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class Applications(Base):
    __tablename__ = 'applications'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    userId = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    postId = Column(Integer, ForeignKey(
        "posts.id", ondelete="CASCADE"), primary_key=True)
    status = Column(Integer, server_default='0', nullable=False)
    owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    recruiterId = Column(Integer, ForeignKey(
        "recruiter_profile.id", ondelete="CASCADE"), nullable=False)
    createdAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
    updatedAt = Column(TIMESTAMP(timezone=True),
                       server_default=text('now()'), nullable=False)
