from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class QQMusic(Base):
    __tablename__ = 'qqmusic'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    song = Column(String)
    singer = Column(String)
    duration = Column(String)
    list_name = Column(String)
    date = Column(String)
    create_at = Column(DateTime, default=func.now())
