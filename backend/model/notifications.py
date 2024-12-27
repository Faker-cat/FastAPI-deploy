from datetime import datetime

from backend.model.base import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, Text
from sqlalchemy.dialects.postgresql import UUID


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自動インクリメント
    user_id = Column(
        UUID, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )  # 通知を受け取るユーザー
    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE")
    )  # 質問への通知
    answer_id = Column(
        Integer, ForeignKey("answers.id", ondelete="CASCADE")
    )  # 回答への通知
    message = Column(Text, nullable=False)  # 通知内容
    is_read = Column(Boolean, default=False)  # 通知が読まれたかどうか
    created_at = Column(
        DateTime, default=datetime.utcnow
    )  # 通知の作成日時（デフォルトで現在時刻）

    # リレーション：User, Question, Answer モデルとの関連を設定
    # user = relationship("User", back_populates="notification")
    # question = relationship("Question", back_populates="notification")
    # answer = relationship("Answer", back_populates="notification")
