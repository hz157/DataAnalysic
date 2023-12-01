"""
Module/Script Name: NetEaseMusic Data API
Author: RyanZhang
Date: 1/12/2023

Description: 网易云音乐接口
Interface_List:

Dependencies:
- sqlalchemy
- pandas

"""
import pandas as pd

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from dependent import mysql

router = APIRouter()


def get_db():
    db = mysql.connectSql()
    try:
        yield db
    finally:
        db.close()
