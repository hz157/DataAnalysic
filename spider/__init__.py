import os
import threading
import platform
import time

from spider import bilibili, neteasemusic, qqmusic

# 判断执行平台
if platform.system() == 'Windows':
    clear_command = 'cls'
elif platform.system() == 'Linux' or platform.system() == 'Darwin':
    clear_command = 'clear'


def run_bilibili():
    bilibili.runBilibiliSpider()


def run_neteastmusic():
    neteasemusic.runNeteastMusicSpider()


def run_qqmusic():
    qqmusic.runQQMusicSpider()


def clear_console():
    while True:
        os.system(clear_command)
        time.sleep(1)

def start_threads():
    # 创建并启动线程
    thread_bilibili = threading.Thread(target=run_bilibili)
    thread_neteastmusic = threading.Thread(target=run_neteastmusic)
    thread_qqmusic = threading.Thread(target=run_qqmusic)
    thread_clear = threading.Thread(target=clear_console)

    # 启动线程
    thread_bilibili.start()
    thread_neteastmusic.start()
    thread_qqmusic.start()
    # thread_clear.start()


# 在模块导入时自动执行
start_threads()
