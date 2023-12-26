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
import os
import uuid
from typing import Optional

import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy import desc, asc, func, and_
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse, FileResponse

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


@router.get("/download_data")
def download_data(type: int = None, db: Session = Depends(get_db)):
    fileName = str(uuid.uuid4()) + ".csv"
    filePath = os.path.join(os.getcwd(), "tmp_file", fileName)
    # 执行SQL查询
    query_result = db.query(BilibiliVideo).all()
    # 获取列名
    columns = query_result[0].__table__.columns.keys() if query_result else []
    if type is None:
        # 将数据转为 Pandas DataFrame
        df = pd.DataFrame([{col: getattr(item, col) for col in columns} for item in query_result])
        # 将 DataFrame 保存为 CSV 文件
        df.to_csv(filePath, index=False)
    else:
        # 将数据转为 Pandas DataFrame
        df = pd.DataFrame([{col: getattr(item, col) for col in columns} for item in query_result])
        # 根据 create_at 列进行降序排序
        df = df.sort_values(by="create_at", ascending=False)
        # 去除重复的 BVID，保留最新的数据
        df = df.drop_duplicates(subset="bvid", keep="first")
        # 将 DataFrame 保存为 CSV 文件
        df.to_csv(filePath, index=False)
    # 设置响应头，告诉浏览器文件类型和文件名
    response = FileResponse(filePath, filename=fileName,
                            media_type="text/csv")
    return response


@router.get("/up_percent")
def get_up_percent(type: int = None, db: Session = Depends(get_db)):
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
