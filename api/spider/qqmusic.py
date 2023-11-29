import random
import time

import requests
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy.exc import NoResultFound
from tqdm import tqdm

from config import HttpParams
from dependent import mysql
from models.qqmusic import QQMusic

session = mysql.connectSql()


def requestsList():
    SoaringList()
    HotSongChart()
    NewSongChart()
    PopIndexChart()
    TencentMusicOriginalList()
    ListeningIdentifyingSongsChart()
    MainlandRankings()
    HongKongRegionList()
    TaiwanList()
    EuropeanAmericanRankings()
    KoreanList()
    JapanChart()
    JOOXLocalHotList()
    HongKongTVBPowerSongGoldChart()
    TaiwanKKBOXList()
    OnlineSongChart()
    DJDanceChart()
    DoukuaiBang()
    VarietyNewSongChart()
    Electronicaudiochart()
    FilmTelevisionGoldenSongChart()
    NationalWindHotSongChart()
    RapChart()
    AnimeMusicChart()
    GameMusicChart()
    KSongGoldenSongChart()
    BillboardListUnitedStates()
    KoreanMelonList()
    UKRankings()
    JapanPublicTrustList()
    YouTubeMusicRankings()
    mysql.closeSql(session)


# 飙升榜
def SoaringList():
    toplist("https://y.qq.com/n/ryqq/toplist/62", "飙升榜")


# 热歌榜
def HotSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/26", "热歌榜")


# 新歌榜
def NewSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/27", "新歌榜")


# 流行指数榜
def PopIndexChart():
    toplist("https://y.qq.com/n/ryqq/toplist/4", "流行指数榜")


# 腾讯音乐人原创榜
def TencentMusicOriginalList():
    toplist("https://y.qq.com/n/ryqq/toplist/52", "腾讯音乐人原创榜")


# 听歌识趣榜
def ListeningIdentifyingSongsChart():
    toplist("https://y.qq.com/n/ryqq/toplist/67", "听歌识趣榜")


# 内地榜
def MainlandRankings():
    toplist("https://y.qq.com/n/ryqq/toplist/5", "内地榜")


# 香港地区榜
def HongKongRegionList():
    toplist("https://y.qq.com/n/ryqq/toplist/59", "香港地区榜")


# 台湾地区榜
def TaiwanList():
    toplist("https://y.qq.com/n/ryqq/toplist/61", "台湾地区榜")


# 欧美榜
def EuropeanAmericanRankings():
    toplist("https://y.qq.com/n/ryqq/toplist/3", "欧美榜")


# 韩国榜
def KoreanList():
    toplist("https://y.qq.com/n/ryqq/toplist/16", "韩国榜")


# 日本榜
def JapanChart():
    toplist("https://y.qq.com/n/ryqq/toplist/17", "日本榜")


# JOOX本地热播榜
def JOOXLocalHotList():
    toplist("https://y.qq.com/n/ryqq/toplist/126", "JOOX本地热播榜")


# 香港TVB劲歌金榜
def HongKongTVBPowerSongGoldChart():
    toplist("https://y.qq.com/n/ryqq/toplist/130", "香港TVB劲歌金榜")


# 台湾KKBOX榜
def TaiwanKKBOXList():
    toplist("https://y.qq.com/n/ryqq/toplist/127", "台湾KKBOX榜")


# 网络歌曲榜
def OnlineSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/28", "网络歌曲榜")


# DJ舞曲榜
def DJDanceChart():
    toplist("https://y.qq.com/n/ryqq/toplist/63", "DJ舞曲榜")


# 抖快榜
def DoukuaiBang():
    toplist("https://y.qq.com/n/ryqq/toplist/60", "抖快榜")


# 综艺新歌榜
def VarietyNewSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/64", "综艺新歌榜")


# 电音榜
def Electronicaudiochart():
    toplist("https://y.qq.com/n/ryqq/toplist/57", "电音榜")


# 影视金曲榜
def FilmTelevisionGoldenSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/29", "影视金曲榜")


# 国风热歌榜
def NationalWindHotSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/65", "国风热歌榜")


# 说唱榜
def RapChart():
    toplist("https://y.qq.com/n/ryqq/toplist/58", "说唱榜")


# 动漫音乐榜
def AnimeMusicChart():
    toplist("https://y.qq.com/n/ryqq/toplist/72", "动漫音乐榜")


# 游戏音乐榜
def GameMusicChart():
    toplist("https://y.qq.com/n/ryqq/toplist/73", "游戏音乐榜")


# K歌金曲榜
def KSongGoldenSongChart():
    toplist("https://y.qq.com/n/ryqq/toplist/36", "K歌金曲榜")


# 美国公告牌榜
def BillboardListUnitedStates():
    toplist("https://y.qq.com/n/ryqq/toplist/108", "美国公告牌榜")


# 韩国Melon榜
def KoreanMelonList():
    toplist("https://y.qq.com/n/ryqq/toplist/129", "韩国Melon榜")


# 英国UK榜
def UKRankings():
    toplist("https://y.qq.com/n/ryqq/toplist/107", "英国UK榜")


# 日本公信榜
def JapanPublicTrustList():
    toplist("https://y.qq.com/n/ryqq/toplist/105", "日本公信榜")


# YouTube音乐排行榜
def YouTubeMusicRankings():
    toplist("https://y.qq.com/n/ryqq/toplist/128", "YouTube音乐排行榜")


def toplist(base_url, name):
    # 随机延迟1-10s
    time.sleep(random.randint(1, 10))
    print(f"sprider: {name}")
    response = requests.get(url=base_url, headers=HttpParams.browser_ua_header)  # 发起http_get请求
    if response.status_code == 200:  # 返回http状态码为200的情况下
        response_soup = BeautifulSoup(response.text, "html.parser")  # 载入bs4
    else:
        return None
    div_elements = response_soup.select("div.songlist__item.songlist__item--even, div.songlist__item")  # 寻找对应的html标签
    date = response_soup.find(name='span', class_="toplist_switch__data").text  # 获取日期
    flag = -1
    for i in date:  # 判断日期格式是否为 11.01-11.07之类的情况
        if "-" == i:
            flag += 1
    if flag == 0:
        date = "第" + str(datetime.strptime(date.split('-')[0], "%m.%d").isocalendar().week) + "周"  # 统一日期格式为 第x周
    total_items = len(div_elements)
    for item in tqdm(div_elements, desc=f"QQMusic {name} Processing", unit="item", total=total_items):  # 构造数据
        div_soup = BeautifulSoup(str(item), "html.parser")  # 载入bs4
        data = QQMusic()
        data.rank = div_soup.select("div.songlist__number songlist__number--top, div.songlist__number ")[0].text  # 获取排名
        data.song = div_soup.select_one("span.songlist__songname_txt a:nth-of-type(2)").get('title')  # 获取歌名
        # 获取歌手名
        # 查找<div class="songlist__artist">元素
        artist_div = div_soup.find('div', {'class': 'songlist__artist'})
        # 找到<div>内的所有<a>标签
        artist_links = artist_div.find_all('a', {'class': 'playlist__author'})
        # 提取每个<a>标签的文本内容
        data.singer = [link.get_text(strip=True) for link in artist_links]
        # 获取歌曲时长
        data.duration = convertTime(div_soup.find(name="div", class_="songlist__time").text)
        # 查找包含特定文本的<a>标签
        song_links = div_soup.find('span', {'class': 'songlist__songname_txt'}).find_all('a')
        # 提取第二个<a>标签的href属性值
        if len(song_links) >= 2:
            data.url = "https://y.qq.com" + song_links[1]['href']
        data.list_name = name  # 获取榜单名称
        data.date = date  # 日期
        data.create_at = datetime.now()
        # 检查该条目是否已存在于数据库中
        try:
            existing_data = session.query(QQMusic).filter(
                QQMusic.rank == data.rank,
                QQMusic.song == data.song,
                QQMusic.url == data.url,
                QQMusic.list_name == data.list_name,
                QQMusic.date == data.date
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


def convertTime(time_str):
    # 分割时间字符串，得到小时和分钟
    hours, minutes = map(int, time_str.split(':'))
    # 计算总分钟数
    total_minutes = hours * 60 + minutes
    # 将总分钟数转换为毫秒
    total_milliseconds = total_minutes * 60 * 1000
    return total_milliseconds
