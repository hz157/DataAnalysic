"""
Module/Script Name: QQMusic Data API
Author: RyanZhang
Date: 1/12/2023

Description: QQ音乐接口
Interface_List:

Dependencies:
- sqlalchemy
- pandas

"""
import json
import math

import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependent import mysql
from models.bilibiliup import BilibiliUp
from models.bilibilivideo import BilibiliVideo
from models.databasemonitor import DatabaseMonitor
from models.neteasemusic import NetEaseMusic
from models.qqmusic import QQMusic
from utils.serialized import encode_custom

router = APIRouter()


def get_db():
    db = mysql.connectSql()
    try:
        yield db
    finally:
        db.close()

@router.get("/welcome")
def welcome(db: Session = Depends(get_db)):
    qq_music_data_count = db.query(QQMusic).count()
    netease_music_data_count = db.query(NetEaseMusic).count()
    bilibili_up_data_count = db.query(BilibiliUp).count()
    bilibili_video_data_count = db.query(BilibiliVideo).count()
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": {
                                     "qq_music": qq_music_data_count,
                                     "netease_music": netease_music_data_count,
                                     "bilibili_up": bilibili_up_data_count,
                                     "bilibili_video": bilibili_video_data_count,
                                 }})  # 数据

@router.get("/db_data")
def get_db_data(num: int = None,db: Session = Depends(get_db)):
    if num is None:
        qq_music_data_count = db.query(DatabaseMonitor).filter_by(type="QQ音乐").order_by(
            desc(DatabaseMonitor.create_at)).first()
        netease_music_data_count = db.query(DatabaseMonitor).filter_by(type="网易云音乐").order_by(
            desc(DatabaseMonitor.create_at)).first()
        bilibili_up_data_count = db.query(DatabaseMonitor).filter_by(type="哔哩哔哩UP主").order_by(
            desc(DatabaseMonitor.create_at)).first()
        bilibili_video_data_count = db.query(DatabaseMonitor).filter_by(type="哔哩哔哩Video").order_by(
            desc(DatabaseMonitor.create_at)).first()
        all_data_count = db.query(DatabaseMonitor).filter_by(type="全库").order_by(
            desc(DatabaseMonitor.create_at)).first()

    else:
        qq_music_data_count = db.query(DatabaseMonitor).filter_by(type="QQ音乐").order_by(
            desc(DatabaseMonitor.create_at)).limit(num).all()
        netease_music_data_count = db.query(DatabaseMonitor).filter_by(type="网易云音乐").order_by(
            desc(DatabaseMonitor.create_at)).limit(num).all()
        bilibili_up_data_count = db.query(DatabaseMonitor).filter_by(type="哔哩哔哩UP主").order_by(
            desc(DatabaseMonitor.create_at)).limit(num).all()
        bilibili_video_data_count = db.query(DatabaseMonitor).filter_by(type="哔哩哔哩Video").order_by(
            desc(DatabaseMonitor.create_at)).limit(num).all()
        all_data_count = db.query(DatabaseMonitor).filter_by(type="全库").order_by(
            desc(DatabaseMonitor.create_at)).limit(num).all()

    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": {
                                     "qq_music": json.loads(json.dumps(qq_music_data_count, default=encode_custom)),
                                     "netease_music": json.loads(json.dumps(netease_music_data_count, default=encode_custom)),
                                     "bilibili_up": json.loads(json.dumps(bilibili_up_data_count, default=encode_custom)),
                                     "bilibili_video": json.loads(json.dumps(bilibili_video_data_count, default=encode_custom)),
                                     "all": json.loads(json.dumps(all_data_count, default=encode_custom))
                                }})  # 数据

@router.get("/percent")
def percent(db: Session = Depends(get_db)):
    qq_music_data_count = db.query(QQMusic).count()
    netease_music_data_count = db.query(NetEaseMusic).count()
    bilibili_up_data_count = db.query(BilibiliUp).count()
    bilibili_video_data_count = db.query(BilibiliVideo).count()
    all = bilibili_video_data_count + netease_music_data_count + qq_music_data_count
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": {
                                     "qq_music": f"{round(qq_music_data_count / all * 100, 3)}",
                                     "netease_music": f"{round(netease_music_data_count / all * 100, 3)}",
                                     "bilibili": f"{round(bilibili_up_data_count / all * 100, 3)}",
                                 }})  # 数据