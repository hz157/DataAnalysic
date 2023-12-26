"""
Module/Script Name: Monitor
Author: RyanZhang
Date: 1/12/2023

Description: 数据库监控

Dependencies:
- sqlalchemy
- requests
- tqdm

"""
import datetime
import json
import random
import time

import requests

from tqdm import tqdm

from config import HttpParams
from dependent import mysql
from models.bilibiliup import BilibiliUp
from models.bilibilivideo import BilibiliVideo
from models.databasemonitor import DatabaseMonitor
from models.neteasemusic import NetEaseMusic
from models.qqmusic import QQMusic

# 连接数据库
session = mysql.connectSql()


def update_date():
    qq_music_data_count = session.query(QQMusic).count()
    data = DatabaseMonitor()
    data.data = qq_music_data_count
    data.type = "QQ音乐"
    data.create_at = datetime.datetime.now()
    insert(data)
    bilibili_up_data_count = session.query(BilibiliUp).count
    data = DatabaseMonitor()
    data.data = bilibili_up_data_count
    data.type = "哔哩哔哩UP主"
    data.create_at = datetime.datetime.now()
    insert(data)
    netease_music_data_count = session.query(NetEaseMusic).count()()
    data = DatabaseMonitor()
    data.data = netease_music_data_count
    data.type = "网易云音乐"
    data.create_at = datetime.datetime.now()
    insert(data)
    bilibili_video_data_count = session.query(BilibiliVideo).count()
    data = DatabaseMonitor()
    data.data = bilibili_video_data_count
    data.type = "哔哩哔哩Video"
    data.create_at = datetime.datetime.now()
    insert(data)
    data = DatabaseMonitor()
    data.data = bilibili_video_data_count + bilibili_up_data_count + qq_music_data_count + netease_music_data_count
    data.type = "全库"
    data.create_at = datetime.datetime.now()


def insert(data):
    # 检查该条目是否已存在于数据库中
    try:
        session.add(data)
        session.commit()
        return True
    except:
        return False
