import json
import requests

from sqlalchemy.exc import NoResultFound

from config import HttpParams
from dependent import mysql
from models.bilibiliup import BilibiliUp

# 连接数据库
session = mysql.connectSql()


def requestsList():
    getUpInfo()
    mysql.closeSql(session)


def getUpInfo(mid):
    relationship_api_url = f"https://api.bilibili.com/x/relation/stat?vmid={mid}"
    upstat_api_url = f"https://api.bilibili.com/x/space/upstat?mid={mid}"

    # 查询数据库是否存在相同mid的数据
    try:
        existing_data = session.query(BilibiliUp).filter_by(mid=mid).one()
    except NoResultFound:
        # 如果数据库中不存在相同mid的数据，则创建一个新实例
        existing_data = BilibiliUp(mid=mid)

    # 获取粉丝数量，关注量
    response = requests.get(url=relationship_api_url, headers=HttpParams.browser_ua_header)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data']['follower'] is not None:
            existing_data.follower = json_data['data']['follower']
        if json_data['data']['following'] is not None:
            existing_data.following = json_data['data']['following']

    # 获取播放量，获赞数量
    response = requests.get(url=upstat_api_url, headers=HttpParams.browser_ua_header)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data']['likes'] is not None:
            existing_data.likes = json_data['data']['likes']
        if json_data['data']['archive']['view'] is not None:
            existing_data.view = json_data['data']['archive']['view']


    # 使用事务进行数据库操作
    try:
        session.add(existing_data)
        session.commit()
    except Exception as e:
        # 处理异常，可以进行回滚等操作
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


