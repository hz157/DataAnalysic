# Spider 
> Default Multithreading Execution, Simultaneously Crawling Data from QQ Music, Netease Cloud Music, and Bilibili Videos

![console_run](https://github.com/hz157/DataAnalysic/blob/8e81eea51d0bbdb748aa08ce98ccae6d511dce83/git_doc/img/spider_multithreading_execution.gif)


## Description
> The spider can run independently

### Independent run
1. Please copy folder api/spider, models, config, and deppendent to create a project
2. Modify API/spider/__ Init__ Introduction of py files
```python
from api.spider import bilibili, neteasemusic, qqmusic
# change 👇
from spider import bilibili, neteasemusic, qqmusic
```
3. create main.py
```python
import spider

if __name__ == "__main__":
    spider_obj = spider
```

### deppendent
- requests~=2.31.0
- PyMySQL~=1.1.0
- tqdm~=4.66.1
- beautifulsoup4~=4.12.2
- sqlalchemy~=2.0.23
```shell
pip install -r requirement.txt

# Creating a virtual environment
python -m venv venv

# Using virtual environments
# -windows Platform
./venv/Scripts/activate
# -Linux Platform
source /venv/bin/activate
```


## Bilibili
![bilibili_console](https://github.com/hz157/DataAnalysic/blob/36b12a90505efb5a97528cb6cff997e6c52dec01/git_doc/img/bilibili_console.gif)
### Accessible Rankings
- up主信息
  - 粉丝数
  - 关注数
  - 视频时长
  - 获赞数
- 每周必看
- 入站必刷
- 综合热门
- 排行榜 

## Netease Music
### Accessible Rankings


## QQ Music
### Accessible Rankings


