from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship
from model import Base


class WordInfo(Base):
    __tablename__ = 'word_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey('word.id'))
    title = Column(String(100), nullable=True)
    content = Column(String(100), nullable=True)

    word = relationship("Word", back_populates="info")
