from backend.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer

# from sqlalchemy.orm import relationship


class QuestionTag(Base):
    __tablename__ = "question_tags"

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )  # 質問ID
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )  # タグID

    # リレーション：質問とタグの多対多の関係を設定
    # question = relationship("Question", back_populates="tags")
    # tag = relationship("Tag", back_populates="questions")
