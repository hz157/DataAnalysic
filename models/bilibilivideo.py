from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class BilibiliVideo(Base):
    __tablename__ = 'bilibili_video'

    id = Column(Integer, primary_key=True)
    title = Column(Integer)
    up = Column(String)
    up_mid = Column(String)
    pub_location = Column(String)
    bvid = Column(String)
    view = Column(Integer)
    danmaku = Column(Integer)
    reply = Column(Integer)
    favorite = Column(Integer)
    coin = Column(Integer)
    share = Column(Integer)
    like = Column(Integer)
    dislike = Column(Integer)
    list_name = Column(String)
    create_at = Column(DateTime, default=func.now())
