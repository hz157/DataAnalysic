"""
Module/Script Name: 序列化工具类
Author: RyanZhang
Date: 1/12/2023

Description: 实体类对象序列化工具类

Dependencies:
- sqlalchemy

"""
from datetime import date, datetime

from sqlalchemy.orm import DeclarativeMeta


# 将对象转换成字典形式
def to_dict(obj):
    return {attr: getattr(obj, attr) for attr in dir(obj)}
    # Remove attributes starting with '__' (internal attributes) and functions/methods
    # valid_attributes = [attr for attr in dir(obj) if not callable(getattr(obj, attr)) and not attr.startswith('__')]
    #
    # # Create a dictionary with valid attributes
    # result_dict = {attr: getattr(obj, attr) for attr in valid_attributes}
    #
    # # Remove newline characters and replace '\\' with '\'
    # result_dict = {key: value.replace('\n', '').replace('\\', '\\').replace('\\', '') if isinstance(value, str) else value for
    #                key, value in result_dict.items()}
    #
    # return result_dict


# 定义自定义编码器函数
def encode_custom(obj):
    if isinstance(obj, (date, datetime)):
        return obj.strftime("%Y-%m-%d %H:%M:%S") if isinstance(obj, datetime) else obj.strftime("%Y-%m-%d")
    elif isinstance(obj.__class__, DeclarativeMeta):
        # If obj is an instance of a SQLAlchemy model
        return {c.name: getattr(obj, c.name) for c in obj.__table__.columns}
    elif hasattr(obj, "to_dict"):
        return obj.to_dict()
    else:
        raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")
    # if isinstance(obj, date):
    #     # 如果对象是日期类型，则返回其格式化后的字符串表示
    #     return obj.strftime("%Y-%m-%d")
    # elif isinstance(obj, DateTime):
    #     # 如果对象是日期类型，则返回其格式化后的字符串表示
    #     return obj.strftime("%Y-%m-%d %H:%M:%S")
    # elif isinstance(obj, JSON):
    #     # 如果对象有to_dict()方法，则调用该方法获取属性字典并返回
    #     return obj
    # elif hasattr(obj, "to_dict"):
    #     # 如果对象有to_dict()方法，则调用该方法获取属性字典并返回
    #     return obj.to_dict()
    # else:
    #     raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")

