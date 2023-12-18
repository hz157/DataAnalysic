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
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependent import mysql
from models.qqmusic import QQMusic
from utils.serialized import encode_custom

router = APIRouter()


def get_db():
    db = mysql.connectSql()
    try:
        yield db
    finally:
        db.close()


@router.get("/music")
def get_video(page: int = 0, num: int = 100, db: Session = Depends(get_db)):
    start = page * num
    if page == 1:
        start = 0
    data = db.query(QQMusic).offset(start).limit(num).all()
    count = db.query(QQMusic).count()
    # 反序列化
    serialized_data = json.dumps(data, default=encode_custom)
    return JSONResponse(content={"code": 0,
                                 "message": "success",
                                 "page": page if page != 0 else page + 1,  # 当前页数
                                 "number": num,  # 单页显示数量
                                 "count": math.ceil(count / num),  # 总页数
                                 "sum": count,  # 数据总量
                                 "data": json.loads(serialized_data)})  # 数据
