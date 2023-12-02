import datetime
import json
import random
import time

import requests

from sqlalchemy.exc import NoResultFound
from tqdm import tqdm

from config import HttpParams
from dependent import mysql
from models.bilibiliup import BilibiliUp
from models.bilibilivideo import BilibiliVideo

# 连接数据库
session = mysql.connectSql()


def runBilibiliSpider():
    getRank()
    getMustSee()
    getWeekHot()
    getComHot()
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
    # print(response.text)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data'].get('follower') is not None:
            existing_data.follower = json_data['data']['follower']
        if json_data['data'].get('following') is not None:
            existing_data.following = json_data['data']['following']

    # 获取播放量，获赞数量
    response = requests.get(url=upstat_api_url, headers=HttpParams.browser_ua_header)
    # print(response.text)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data'].get('likes') is not None:
            existing_data.likes = json_data['data']['likes']
        # 获取 'archive' 字典
        archive_data = json_data['data'].get('archive')

        # 检查 'archive_data' 是否存在，并获取其 'view' 值
        if archive_data is not None:
            view = archive_data.get('view')
            if view is not None:
                existing_data.view = view

    # 使用事务进行数据库操作
    try:
        session.add(existing_data)
        session.commit()
    except Exception as e:
        # 处理异常，可以进行回滚等操作
        session.rollback()
        print(f"Error: {e}")
    # finally:
    #     session.close()


# 解析json数据
def analysic_json_data(json_data, list_name):
    data = BilibiliVideo()
    data.title = json_data['title']
    data.up = json_data['owner']['name']
    data.up_mid = json_data['owner']['mid']
    if json_data.get('pub_location'):
        data.pub_location = json_data['pub_location']
    data.bvid = json_data['bvid']
    data.view = json_data['stat']['view']
    data.danmaku = json_data['stat']['danmaku']
    data.reply = json_data['stat']['reply']
    data.favorite = json_data['stat']['favorite']
    data.coin = json_data['stat']['coin']
    data.share = json_data['stat']['share']
    data.like = json_data['stat']['like']
    data.dislike = json_data['stat']['dislike']
    data.list_name = list_name
    data.create_at = datetime.datetime.now()
    # 使用事务进行数据库操作
    try:
        session.add(data)
        session.commit()
    except Exception as e:
        # 处理异常，可以进行回滚等操作
        session.rollback()
        print(f"Error: {e}")
    finally:
        session.close()


# 综合热门视频
def getComHot():
    for page in range(1, 51):
        url = f"https://api.bilibili.com/x/web-interface/popular?ps=10&pn={page}"
        response = requests.get(url=url, headers=HttpParams.browser_ua_header)
        json_data = json.loads(response.text)
        total_items = len(json_data['data']['list'])
        for item in tqdm(json_data['data']['list'], desc=f"Bilibili Comprehensive Popular(number: {page}) Processing",
                         unit="item", total=total_items):
            analysic_json_data(item, "综合热门")
        time.sleep(random.randint(1, 10))  # 随机延时


# 入站必刷
def getMustSee():
    url = "https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&pn=1"
    response = requests.get(url=url, headers=HttpParams.browser_ua_header)
    json_data = json.loads(response.text)

    total_items = len(json_data['data']['list'])
    for item in tqdm(json_data['data']['list'], desc="Bilibili Must-Watch for Newcomers Processing", unit="item",
                     total=total_items):
        analysic_json_data(item, "入站必刷")


# 每周热门
def getWeekHot():
    page = 1
    while True:
        url = f"https://api.bilibili.com/x/web-interface/popular/precious?page_size=100&pn={page}"
        response = requests.get(url=url, headers=HttpParams.browser_ua_header)
        json_data = json.loads(response.text)
        # 啊B程序员在超过期数会返回啥都木有，可爱捏
        if json_data['code'] == -404 or json_data['message'] == "啥都木有":
            print('向你转达啊B程序员的敬意: 啥都木有')
            return
        else:
            total_items = len(json_data['data']['list'])
            for item in tqdm(json_data['data']['list'], desc=f"Bilibili Weekly Popular(Number: {page}) Processing",
                             unit="item", total=total_items):
                analysic_json_data(item, "每周热门")
            page += 1
        time.sleep(random.randint(1, 10))  # 随机延时


# 排行榜
def getRank():
    url = "https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
    response = requests.get(url=url, headers=HttpParams.browser_ua_header)
    json_data = json.loads(response.text)
    total_items = len(json_data['data']['list'])
    for item in tqdm(json_data['data']['list'], desc="Bilibili Rankings Processing", unit="item", total=total_items):
        analysic_json_data(item, "排行榜")
