from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from models.db import Base


class GitHubAuth(Base):
    __tablename__ = "github_auths"

    id = Column(Integer, primary_key=True, index=True)
    github_id = Column(String, unique=True, index=True)
    access_token = Column(String)
    refresh_token = Column(String)
    token_expires_at = Column(DateTime)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    # One-to-one relationship with User
    user = relationship("User", back_populates="github_auth")
