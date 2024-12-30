from datetime import datetime, timedelta

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from backend.model.answers import Answer  # noqa
from backend.model.base import Base
from backend.model.bookmarks import Bookmark  # noqa
from backend.model.likes import Like  # noqa
from backend.model.notifications import Notification  # noqa
from backend.model.tags import Tag, TagSchema  # noqa
from backend.model.users import User  # noqa


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)  # 質問のタイトル
    user_id = Column(UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)  # 投稿者
    is_anonymous = Column(Boolean, default=True)  # 匿名フラグ
    content = Column(Text, nullable=False)  # 質問の本文
    created_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(hours=9))  # 作成日時

    # リレーションシップ
    user = relationship("User", backref="question")
    answer = relationship("Answer", backref="question")
    tags = relationship("Tag", secondary="question_tags", backref="question")
    likes = relationship("Like", backref="question")
    bookmarks = relationship("Bookmark", backref="question")
    notifications = relationship("Notification", backref="question")


class QuestionSchema(BaseModel):
    title: str
    user_id: str
    is_anonymous: bool
    content: str
    tags: list[TagSchema] = []

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True

    # def __init__(
    #     self,
    #     title: str,
    #     user_id: uuid.UUID,
    #     body: str,
    #     is_anonymous: bool = True,
    # ):
    #     self.title = title
    #     self.user_id = user_id
    #     self.body = body
    #     self.is_anonymous = is_anonymous
