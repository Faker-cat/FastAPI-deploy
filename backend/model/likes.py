from datetime import datetime, timedelta

from backend.model.base import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # いいねしたユーザー
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE")
    )  # 質問へのいいね
    answer_id = Column(
        Integer, ForeignKey("answers.id", ondelete="CASCADE")
    )  # 回答へのいいね
    created_at = Column(
        DateTime, default=lambda: datetime.utcnow() + timedelta(hours=9)
    )  # いいねの作成日時（デフォルトで現在時刻）

    # リレーション：User、Question、Answer モデルとの関連を設定
    # user = relationship("User", back_populates="like")
    # question = relationship("Question", back_populates="like")
    # answer = relationship("Answer", back_populates="like")
