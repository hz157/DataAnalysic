from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class NetEaseMusic(Base):
    __tablename__ = 'neteasemusic'

    id = Column(Integer, primary_key=True)
    rank = Column(Integer)
    song = Column(String)
    singer = Column(JSON)
    duration = Column(Integer)
    list_name = Column(String)
    url = Column(String)
    date = Column(String)
    create_at = Column(DateTime, default=func.now())
