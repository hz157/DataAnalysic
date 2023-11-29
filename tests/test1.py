import requests
from bs4 import BeautifulSoup
import datetime

from api.spider import bilibili
from config import HttpParams

if __name__ == "__main__":
    for i in range(1000,1999):
        bilibili.getUpInfo(i)
    # url = "https://www.bilibili.com/v/popular/rank/all"
    # page_text = requests.get(url=url, headers=HttpParams.browser_ua_header).text
    # soup = BeautifulSoup(page_text, "lxml")
    # li_list = soup.select(".rank-list > li")
    # with open("bZhanRank_bs4.txt", "w", encoding="utf-8") as fp:
    #     fp.write("当前爬取热榜的时间为：" + str(datetime.datetime.now()) + "")
    #     for li in li_list:
    #         # 解析视频排行
    #         li_rank = li.find("div", class_="num").string
    #         li_rank = "视频排行为：" + li_rank + ","
    #         # 解析视频标题
    #         li_title = li.find("div", class_="info").a.string.strip()
    #         li_title = "视频标题为：" + li_title + ","
    #         # 解析视频播放量
    #         li_viewCount = li.select(".detail>span")[0].text.strip()
    #         li_viewCount = "视频播放量为：" + li_viewCount + ", "
    #         # 解析弹幕数量
    #         li_danmuCount = li.select(".detail>span")[1].text.strip()
    #         li_danmuCount = "视频弹幕数量为：" + li_danmuCount + ", "
    #         # 解析视频作者
    #         li_upName = li.find("span", class_="data-box up-name").text.strip()
    #         li_upName = "视频up主：" + li_upName + ", "
    #         # 解析综合评分
    #         li_zongheScore = li.find("div", class_="pts").div.string
    #         li_zongheScore = "视频综合得分为:" + li_zongheScore
    #         fp.write(li_rank + li_title + li_viewCount + li_danmuCount + li_upName + li_zongheScore + "")
