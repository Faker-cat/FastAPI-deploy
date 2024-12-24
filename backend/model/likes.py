from backend.model.base import Base
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship


class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)

    user = relationship("User", back_populates="likes")
    item = relationship("Item", back_populates="likes")

    def __init__(self, user_id: int, item_id: int):
        self.user_id = user_id
        self.item_id = item_id
