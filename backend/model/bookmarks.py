import uuid
from datetime import datetime

from backend.model.base import Base
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID


class Bookmark(Base):
    __tablename__ = "bookmarks"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自動インクリメント
    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # ブックマークしたユーザー
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), nullable=False
    )  # ブックマークした質問
    created_at = Column(
        DateTime, default=datetime.utcnow
    )  # ブックマーク作成日時（デフォルトで現在時刻）

    # リレーション：User と Question モデルとの関連を設定
    # user = relationship("User", back_populates="bookmark")
    # question = relationship("Question", back_populates="bookmark")


class BookmarkSchema(BaseModel):
    id: int
    user_id: uuid.UUID

    class Config:
        arbitrary_types_allowed = True
        from_attributes = True
