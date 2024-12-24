from backend.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class QuestionTag(Base):
    __tablename__ = "question_tags"

    question_id = Column(
        Integer, ForeignKey("questions.id", ondelete="CASCADE"), primary_key=True
    )
    tag_id = Column(
        Integer, ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True
    )

    question = relationship("Question", back_populates="tags")
    tag = relationship("Tag", back_populates="questions")

    def __init__(self, question_id: int, tag_id: int):
        self.question_id = question_id
        self.tag_id = tag_id
