from backend.model.base import Base
from backend.model.question_tags import QuestionTag  # noqa
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)  # 自動インクリメント
    name = Column(
        String(50), unique=True, nullable=False
    )  # タグ名（ユニーク、NOT NULL）


class TagSchema(BaseModel):
    id: int
    name: str

    # 多対多のリレーション：質問との関連を定義
    # questions = relationship(
    #     "Question", secondary="question_tags", back_populates="tag"
    # )
