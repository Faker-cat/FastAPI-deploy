from datetime import datetime

from backend.model.base import Base
from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class SearchKeyword(Base):
    __tablename__ = "search_keywords"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    keyword = Column(String(255))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    user = relationship("User", back_populates="search_keywords")

    def __init__(self, user_id: int, keyword: str):
        self.user_id = user_id
        self.keyword = keyword
