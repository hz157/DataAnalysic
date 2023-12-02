"""
Module/Script Name: Bilibili Data API
Author: RyanZhang
Date: 2/12/2023

Description: B站视频接口
Interface_List:
- 分页返回数据
- 发布地区数据分析
- UP主上榜次数排名
- 获取up主信息

Dependencies:
- sqlalchemy
- pandas

"""
import json
import math
from typing import Optional

import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependent import mysql
from models.bilibiliup import BilibiliUp
from models.bilibilivideo import BilibiliVideo
from utils.serialized import encode_custom

router = APIRouter()


def get_db():
    db = mysql.connectSql()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def hello():
    return JSONResponse({"code": 0,
                         "message": "success",
                         "data": "flag{https://github.com/hz157/DataAnalysic}"})


# 获取所有视频
@router.get("/video")
def get_video(page: int = 0, num: int = 100, db: Session = Depends(get_db)):
    start = page * num
    if page == 1:
        start = 0
    data = db.query(BilibiliVideo).offset(start).limit(num).all()
    count = db.query(BilibiliVideo).count()
    # 序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "page": page if page != 0 else page + 1,  # 当前页数
                                 "number": num,  # 单页显示数量
                                 "count": math.ceil(count / num),  # 总页数
                                 "data": json.loads(serialized_data)})  # 数据


# 热门发布地
@router.get("/hot_pub_location")
def hot_pub_location(db: Session = Depends(get_db)):
    # 获取全部带有发布地址的数据
    dataList = db.query(BilibiliVideo.bvid, BilibiliVideo.pub_location).filter(BilibiliVideo.pub_location != None).all()

    # 转换为 DataFrame
    df = pd.DataFrame(dataList, columns=['bvid', 'pub_location'])

    # 过滤掉重复的 bvid
    df = df.drop_duplicates(subset='bvid')
    # 统计每个发布地址的数量
    location_counts = df['pub_location'].value_counts()
    # 获取前 500 个发布地址
    top_locations = location_counts.head(500)

    # 转换为字典
    top_locations = top_locations.to_dict()

    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": top_locations})


# up主上榜次数
@router.get("/up_rank_count")
def up_rank_count(page: Optional[int] = None, num: Optional[int] = None, db: Session = Depends(get_db)):
    # 获取全部带有发布地址的数据
    dataList = db.query(BilibiliVideo.bvid, BilibiliVideo.up).all()
    # 转换为 DataFrame
    df = pd.DataFrame(dataList, columns=['bvid', 'up'])
    # 过滤掉重复的 bvid
    df = df.drop_duplicates(subset='bvid')
    # 统计每个up的数量
    location_counts = df['up'].value_counts()
    # 使用 reset_index 重置索引，并通过 index 属性获取排名
    location_counts_top = location_counts.reset_index()
    location_counts_top['rank'] = location_counts_top.index + 1
    # 转换为字典
    top_locations = location_counts_top.to_dict(orient='records')
    # 数据总量
    all_count = len(top_locations)
    if page is None and num is None:
        return JSONResponse(content={"code": 0,
                                     "message": "success",
                                     "data": top_locations})
    else:
        start = page * num
        if page == 1:
            start = 1

        # 取出排名在 start 至 start+num 之间的数据
        location_counts_between = location_counts_top.iloc[start - 1: start - 1 + num]

        # 转换为字典
        top_locations = location_counts_between.to_dict(orient='records')

        return JSONResponse(content={"code": 0,
                                     "message": "success",
                                     "page": page if page != 0 else page + 1,  # 当前页数
                                     "number": num,  # 单页显示数量
                                     "count": math.ceil(all_count / num),  # 总页数
                                     "data": top_locations})


# 获取up主信息
@router.get("/up_info")
def up_info(mid: Optional[str] = None, num: Optional[int] = None, db: Session = Depends(get_db)):
    if mid is None:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "少侠你是否忘了什么东西？"})
    if num is None:
        num = 10
    # 获取全部数据
    data = db.query(BilibiliUp).filter(BilibiliUp.mid == mid).order_by(desc(BilibiliUp.update_time)).limit(num).all()
    # 序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": json.loads(serialized_data)})
