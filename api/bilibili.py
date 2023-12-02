"""
Module/Script Name: Bilibili Data API
Author: RyanZhang
Date: 1/12/2023

Description: B站视频接口
Interface_List:
- 分页返回数据
- 发布地区数据分析

Dependencies:
- sqlalchemy
- pandas

"""
import json
import math

import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependent import mysql
from models.bilibilivideo import BilibiliVideo
from utils.serialized import encode_custom

router = APIRouter()


def get_db():
    db = mysql.connectSql()
    try:
        yield db
    finally:
        db.close()


@router.get("/video")
def get_video(page: int = 0, num: int = 100, db: Session = Depends(get_db)):
    start = page * num
    if page == 1:
        start = 0
    data = db.query(BilibiliVideo).offset(start).limit(num).all()
    count = db.query(BilibiliVideo).count()
    # 反序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "page": page if page != 0 else page + 1,  # 当前页数
                                 "number": num,  # 单页显示数量
                                 "count": math.ceil(count / num),  # 总页数
                                 "data": json.loads(serialized_data)})  # 数据


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

    # Convert NumPy types to standard Python types
    top_locations = top_locations.to_dict()

    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": top_locations})
