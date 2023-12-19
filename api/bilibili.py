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
from sqlalchemy import desc, asc, func, and_
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
                                 "sum": count,  # 数据总量
                                 "data": json.loads(serialized_data)})  # 数据


@router.get("/only_video")
def get_only_video(page: int = 0, num: int = 100, db: Session = Depends(get_db)):
    start = page * num
    if page == 1:
        start = 0
    # 在查询时只选择需要的字段
    # data = db.query(BilibiliVideo).order_by(desc(BilibiliVideo.create_at)).offset(start).limit(num).all()
    subquery = (
        db.query(
            func.max(BilibiliVideo.create_at).label("max_create_at"),
            BilibiliVideo.bvid
        )
        .group_by(BilibiliVideo.bvid)
        .subquery()
    )

    # 获取经过去重和筛选后的数据总量
    total_filtered_count = (
        db.query(func.count().label("count"))
        .select_from(subquery)
        .scalar()
    )

    data = (
        db.query(BilibiliVideo)
        .join(subquery,
              and_(BilibiliVideo.create_at == subquery.c.max_create_at, BilibiliVideo.bvid == subquery.c.bvid))
        .order_by(desc(BilibiliVideo.create_at))
        .offset(start)
        .limit(num)
        .all()
    )

    ### 废弃 使用pandas， 可能是由于变量类型不对，导致报错，不再修复
    # 将数据转换为 Pandas DataFrame
    # df = pd.DataFrame(data, columns=["bvid", "create_at", ...])
    # df = pd.DataFrame([row.__dict__ for row in data])
    # # 根据 'bvid' 列进行去重，保留最新的数据
    # df_unique = df.sort_values(by='create_at', ascending=False).drop_duplicates(subset='bvid')
    # 将结果转换为 JSON 格式
    # serialized_data = df_unique.to_dict(orient='records')

    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "page": page if page != 0 else page + 1,  # 当前页数
                                 "number": num,  # 单页显示数量
                                 "count": math.ceil(total_filtered_count / num),  # 总页数
                                 "sum": total_filtered_count,  # 数据总量
                                 "data": json.loads(serialized_data)})  # 数据


@router.get("/bvid")
def get_bvid(bvid: str, db: Session = Depends(get_db)):
    if bvid is None:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "参数错误"})  # 数据
    data = db.query(BilibiliVideo).filter(BilibiliVideo.bvid == bvid).all()
    # 反序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": json.loads(serialized_data)})  # 数据


@router.get("/up_count")
def get_up_count(uid: str, db: Session = Depends(get_db)):
    if uid is None:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "参数错误"})  # 数据
    dataList = db.query(BilibiliVideo.bvid, BilibiliVideo.up_mid).filter(BilibiliVideo.up_mid == uid).all()
    # 转换为 DataFrame
    df = pd.DataFrame(dataList, columns=['bvid', 'up_mid'])
    # 过滤掉重复的 bvid
    df = df.drop_duplicates(subset='bvid')
    # 反序列化
    data = db.query(BilibiliUp).filter(BilibiliUp.mid == uid).order_by(desc(BilibiliUp.update_time)).limit(12).all()
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "count": len(df),
                                 "data": json.loads(serialized_data)
                                 })  # 数据


@router.get("/up_percent")
def get_up_percent(type: int=None ,db: Session = Depends(get_db)):
    # 执行SQL查询
    query_result = db.query(BilibiliVideo).all()
    # 将查询结果转换为 Pandas DataFrame
    df = pd.DataFrame([(item.bvid, item.up, item.up_mid) for item in query_result], columns=['bvid', 'up', 'up_mid'])
    # 去除重复的 'bvid' 数据，保留最后一个 'up' 信息
    df_unique = df.sort_values('up').drop_duplicates(subset='bvid', keep='last')
    # 获取每个 'up_mid' 上榜次数
    up_mid_counts = df_unique['up_mid'].value_counts()
    # 获取排行榜前 10 的 'up_mid' 及对应的 'up' 信息
    top_10_up_mid_info = []
    for up_mid, count in up_mid_counts.head(10).items():
        up_info = df_unique[df_unique['up_mid'] == up_mid]['up'].iloc[0]  # 获取 up 信息，这里简单地选择第一个
        top_10_up_mid_info.append({'count': count, 'up': up_info})
    sum_counts = 0
    for item in top_10_up_mid_info:
        sum_counts += item['count']
    if type is None:
        for item in top_10_up_mid_info:
            item['count'] = round((item['count'] / sum_counts) * 100, 3)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "data": top_10_up_mid_info})


@router.get("/up_info")
def get_up_info(uid: str, type: int = 0, db: Session = Depends(get_db)):
    if uid is None:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "参数错误"})  # 数据
    if type == 0:
        dataList = db.query(BilibiliUp).filter(BilibiliUp.mid == uid).order_by(desc(BilibiliUp.update_time)).first()
    else:
        dataList = db.query(BilibiliUp).filter(BilibiliUp.mid == uid).order_by(asc(BilibiliUp.update_time)).all()
    serialized_data = json.dumps(dataList, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
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
