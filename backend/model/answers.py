from datetime import datetime, timedelta

from backend.model.base import Base
from pydantic import BaseModel
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship


class Answer(Base):
    __tablename__ = "answers"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自動インクリメント
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )  # 質問ID
    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # 投稿者ID
    is_anonymous = Column(Boolean, default=True)  # 匿名フラグ（デフォルトTrue）
    content = Column(Text, nullable=False)  # 回答の本文（NOT NULL）
    created_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=9)
    )  # 回答日時（デフォルト現在時刻）

    # リレーション：Question と User との関連を定義
    # question = relationship("Question", backref="answer")
    # user = relationship("User", backref="answer")
    likes = relationship("Like", backref="answer")
    notifications = relationship("Notification", backref="answer")


class AnswerSchema(BaseModel):
    id: int
    question_id: int
    user_id: str
    is_anonymous: bool
    content: str
    created_at: datetime

    class Config:
        arbitrary_types_allowed = True
        orm_mode = True
