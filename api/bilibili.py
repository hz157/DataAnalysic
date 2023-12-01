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
def get_video(skip: int = 0, limit: int = 50, db: Session = Depends(get_db)):
    skip = skip * limit
    data = db.query(BilibiliVideo).offset(skip).limit(limit).all()
    # 反序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "page": skip + 1,
                                 "number": limit,
                                 "data": json.loads(serialized_data)})
    # return data


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

    return JSONResponse(content={"code": 0, "message": "success", "data": top_locations})
