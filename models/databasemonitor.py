from sqlalchemy import Column, Integer, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class DatabaseMonitor(Base):
    __tablename__ = 'database_monitor'

    id = Column(Integer, primary_key=True)
    data = Column(Integer)
    type = Column(String)
    create_at = Column(DateTime, default=func.now())
