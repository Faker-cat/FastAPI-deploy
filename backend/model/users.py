import uuid
from datetime import datetime, timedelta

from backend.model.base import Base
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    display_name = Column(String(50), unique=False, nullable=False)
    bio = Column(Text)
    created_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=9)
    )

    # 質問とのリレーション
    # questions = relationship("Question", back_populates="user")
    answers = relationship("Answer", backref="user")
    likes = relationship("Like", backref="user")
    bookmarks = relationship("Bookmark", backref="user")
    notifications = relationship("Notification", backref="user")


class UserSchema(BaseModel):
    id: uuid.UUID
    display_name: str
    bio: str

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
