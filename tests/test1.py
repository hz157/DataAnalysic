import json
import random
import time

import requests
from tqdm import tqdm

from config import HttpParams
from dependent import mysql
from models.bilibiliup import BilibiliUp


def getUpInfo(session, mid):
    relationship_api_url = f"https://api.bilibili.com/x/relation/stat?vmid={mid}"
    upstat_api_url = f"https://api.bilibili.com/x/space/upstat?mid={mid}"
    data = BilibiliUp()
    data.mid = mid
    # 获取粉丝数量，关注量
    response = requests.get(url=relationship_api_url, headers=HttpParams.browser_ua_header)
    # print(response.text)
    # print(response.text)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data'].get('follower') is not None:
            # existing_data.follower = json_data['data']['follower']
            data.follower = json_data['data']['follower']
        if json_data['data'].get('following') is not None:
            # existing_data.following = json_data['data']['following']
            data.following = json_data['data']['following']

    # 获取播放量，获赞数量
    response = requests.get(url=upstat_api_url, headers=HttpParams.browser_ua_header)
    # print(response.text)
    if response.status_code == 200:
        json_data = json.loads(response.text)
        if json_data['data'].get('likes') is not None:
            # existing_data.likes = json_data['data']['likes']
            data.likes = json_data['data']['likes']
        # 获取 'archive' 字典
        archive_data = json_data['data'].get('archive')

        # 检查 'archive_data' 是否存在，并获取其 'view' 值
        if archive_data is not None:
            view = archive_data.get('view')
            if view is not None:
                # existing_data.view = view
                data.view = view

    # 使用事务进行数据库操作
    try:
        # session.add(existing_data)
        session.add(data)
        session.commit()
    except Exception as e:
        # 处理异常，可以进行回滚等操作
        session.rollback()
        print(f"Error: {e}")


if __name__ == "__main__":
    # for i in range(10000000, 19999999):
    #     bilibili.getUpInfo(i)
    #     time.sleep(3)
    session = mysql.connectSql()
    total_iterations = 99999999 - 10000000 + 1

    # 创建 tqdm 对象，设置总数为 total_iterations
    progress_bar = tqdm(total=total_iterations, desc="Processing")

    for i in range(10000000, 99999999):
        # Your code here
        getUpInfo(session, i)
        time.sleep(random.randint(1, 3))

        # 更新 tqdm 进度条
        progress_bar.update(1)

    # 关闭 tqdm 进度条
    progress_bar.close()
