from datetime import datetime, timedelta
from typing import List

from backend.model.answers import Answer  # noqa
from backend.model.base import Base
from backend.model.bookmarks import BookmarkSchema
from backend.model.likes import LikeSchema
from backend.model.notifications import Notification  # noqa
from backend.model.tags import Tag, TagSchema  # noqa
from backend.model.users import UserSchema
from pydantic import BaseModel
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)  # 質問のタイトル
    user_id = Column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # 投稿者
    is_anonymous = Column(Boolean, default=True)  # 匿名フラグ
    content = Column(Text, nullable=False)  # 質問の本文
    created_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=9)
    )  # 作成日時

    # リレーションシップ
    user = relationship("User", backref="question")
    answer = relationship("Answer", backref="question")
    tags = relationship("Tag", secondary="question_tags", backref="question")
    likes = relationship("Like", backref="question")
    bookmarks = relationship("Bookmark", backref="question")
    notifications = relationship("Notification", backref="question")


class QuestionSchema(BaseModel):
    id: int
    title: str
    user: UserSchema
    is_anonymous: bool
    content: str
    created_at: datetime
    tags: List[TagSchema] = []
    likes: List[LikeSchema]
    bookmarks: List[BookmarkSchema]

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
