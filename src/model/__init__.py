from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config import config

Base = declarative_base()
engine = create_engine(config['SQLALCHEMY_DATABASE_URI'])
Base.metadata.create_all(engine)
session_maker = sessionmaker(bind=engine)
