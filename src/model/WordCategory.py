from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from model import Base


class WordCategory(Base):
    __tablename__ = 'word_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)

    words = relationship("Word", back_populates="category")
