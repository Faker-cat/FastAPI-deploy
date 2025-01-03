from backend.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer


class QuestionTag(Base):
    __tablename__ = "question_tags"

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )  # 質問ID
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )  # タグID
