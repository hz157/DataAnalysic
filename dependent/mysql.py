from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from config import MySQLConf


def connectSql():
    # MySQL数据库
    engine = create_engine(MySQLConf.sql_engine)
    # 创建会话
    session = Session(engine)
    return session


def closeSql(session):
    # 关闭MySQL数据库
    session.close()