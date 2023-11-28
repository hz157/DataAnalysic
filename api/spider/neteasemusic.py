import json
import random
import re
import time

import requests
import platform
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy.exc import NoResultFound

from config import HttpParams
from dependent import mysql
from models.neteasemusic import NetEaseMusic

system_platform = platform.system()

# # 指定浏览器驱动的路径，例如ChromeDriver的路径
# if system_platform == "Linux":
#     driver_path = r'driver/chromedriver-linux64'
#     # driver_path = r'/driver/chromedriver-linux64/chromedriver'
# elif system_platform == "Windows":
#     driver_path = r'driver/chromedriver-win64'
#     # driver_path = r'/driver/chromedriver-win64/chromedriver.exe'
# elif system_platform == "Darwin":
#     driver_path = r'driver/chromedriver-mac-x64'
#     # driver_path = r'/driver/chromedriver-mac-x64/chromedriver'


# 连接数据库
session = mysql.connectSql()


def requestsList():
    getUrl()
    mysql.closeSql(session)


# 获取所有榜单URL
def getUrl():
    response = requests.get(url="https://music.163.com/discover/toplist", headers=HttpParams.browser_ua_header)
    if response.status_code == 200:  # 返回http状态码为200的情况下
        response_soup = BeautifulSoup(response.text, "html.parser")  # 载入bs4
    else:
        return None
    div_element = response_soup.find("div", class_="g-sd3 g-sd3-1")
    ul_element = div_element.find_all("ul", class_="f-cb")
    for item in ul_element:
        li_element = item.find_all("li")
        for li_item in li_element:
            # 在<p>标签中查找<a>标签
            a_tag = li_item.find('a', class_='s-fc0')
            print(f"spider: {a_tag.text}")
            # 提取榜单名称及url
            data = {'name': a_tag.text, 'url': "https://music.163.com" + a_tag['href']}
            toplist(data['url'], data['name'])
            # 随机延迟1-10s
            time.sleep(random.randint(1, 10))


def toplist(base_url, name):
    response = requests.get(url=base_url, headers=HttpParams.browser_ua_header)
    if response.status_code == 200:  # 返回http状态码为200的情况下
        response_soup = BeautifulSoup(response.text, "html.parser")  # 载入bs4
    else:
        return None
    # 使用BeautifulSoup解析页面
    json_data = json.loads(response_soup.find(name="textarea", attrs={"id": "song-list-pre-data"}).text)
    # 查找<meta>标签
    meta_tag = response_soup.find('meta', {'name': 'description'})
    # 提取content属性的值
    content_value = meta_tag['content']
    match = re.search(r'(\d+)月(\d+)日', content_value)
    if match:
        current_year = datetime.now().year
        month = match.group(1)
        day = match.group(2)
        # 构建日期字符串
        date = f'{current_year}-{month.zfill(2)}-{day.zfill(2)}'
    count = 1
    for item in json_data:  # 构造数据
        data = NetEaseMusic()
        data.rank = count  # 获取排名
        count += 1
        data.song = item['name']  # 获取歌名
        data.singer = [artist['name'] for artist in item.get('artists', [])]  # 获取歌手名
        data.duration = item['duration']  # 获取歌曲时长
        data.url = "https://music.163.com/#/song?id=" + str(item['id'])
        data.list_name = name  # 获取榜单名称
        data.date = date  # 日期
        data.create_at = datetime.now()
        # 检查该条目是否已存在于数据库中
        try:
            existing_data = session.query(NetEaseMusic).filter(
                NetEaseMusic.rank == data.rank,
                NetEaseMusic.song == data.song,
                NetEaseMusic.url == data.url,
                NetEaseMusic.list_name == data.list_name,
                NetEaseMusic.date == data.date
            ).first()
            # 条目不存在，添加新条目
            if existing_data is None:
                session.add(data)
                session.commit()

            # 条目已存在，丢弃更改
            # 例如，您可以更新“create_at”字段并提交更改
            # existing_data.create_at = datetime.now()
            # session.commit()
        except NoResultFound:
            # 条目不存在，请将其添加到数据库
            session.add(data)
            session.commit()
