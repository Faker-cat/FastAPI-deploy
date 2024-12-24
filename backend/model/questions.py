import uuid
from datetime import datetime

from backend.model.base import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    user_id = Column(UUID, ForeignKey("users.id"), nullable=False)  # ユーザーのIDを参照
    is_anonymous = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    likes = Column(Integer, default=0)
    bookmarks = Column(Integer, default=0)
    is_liked = Column(Boolean, default=False)
    is_bookmarked = Column(Boolean, default=False)
    tags = Column(ARRAY(String), nullable=False)  # タグは配列として保存

    # リレーション（Userとの関連）
    user = relationship("User", back_populates="questions")

    def __init__(
        self,
        user_name: str,
        title: str,
        content: str,
        user_id: uuid.UUID,
        is_anonymous: bool,
        tags: list,
    ):
        self.user_name = user_name
        self.title = title
        self.content = content
        self.user_id = user_id
        self.is_anonymous = is_anonymous
        self.tags = tags
