"""
Module/Script Name: User API
Author: RyanZhang
Date: 1/12/2023

Description: 用户接口
Interface_List:

Dependencies:
- sqlalchemy
- pandas

"""
import json
import math

from pydantic import BaseModel
from sqlalchemy import and_

from models.user import User
from utils.token import create_access_token

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

class LoginRequest(BaseModel):
    uid: str
    password: str

@router.post("/login")
def login(login_request: LoginRequest, db: Session = Depends(get_db)):
    uid = login_request.uid
    password = login_request.password
    print(uid, password)
    if uid is None or password is None:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "参数不齐"})  # 数据

    data = db.query(User).filter(and_(User.id == uid, User.password == password)).first()
    if data is not None:
        access_token = create_access_token(data={"uid": uid})
        return JSONResponse(content={"code": 0,
                                     "message": "success",
                                     "data": {
                                         "token": access_token,
                                         "userInfo": {
                                             "uid": uid,
                                             "username": data.username,
                                             "last_login_time": str(data.last_login_time),
                                             "last_login_ip": data.last_login_ip
                                         }
                                     }
                                     })
    else:
        return JSONResponse(content={"code": -1,
                                     "message": "fail",
                                     "data": "账号或密码有误"})  # 数据

