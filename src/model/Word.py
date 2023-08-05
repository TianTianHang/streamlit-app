from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from model import Base


class Word(Base):
    __tablename__ = 'word'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    category_id = Column(Integer, ForeignKey('word_category.id'))

    category = relationship("WordCategory", back_populates="words")
    info = relationship("WordInfo", back_populates="word")
