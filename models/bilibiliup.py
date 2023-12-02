from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BilibiliUp(Base):
    __tablename__ = 'bilibili_up'

    id = Column(Integer, primary_key=True)
    mid = Column(String)
    view = Column(Integer)
    likes = Column(Integer)
    following = Column(Integer)
    follower = Column(Integer)
    update_time = Column(DateTime, default=func.now())