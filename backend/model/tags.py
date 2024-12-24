from backend.model.base import Base
from sqlalchemy import Column, Integer, String


class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), unique=True, nullable=False)

    def __init__(self, name: str):
        self.name = name
