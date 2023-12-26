from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional

# 密钥，仅用于演示目的，实际应用中需要更安全的方式保存和管理密钥
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# 生成 Token 的函数
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# OAuth2PasswordBearer 是 FastAPI 内置的一个类，用于处理获取 Token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# 解析 Token 的函数
def decode_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise credentials_exception




# # 被保护的资源，只有在请求中包含有效 Token 时才能访问
# @app.get("/protected")
# async def protected_route(token: str = Depends(oauth2_scheme)):
#     return {"message": "You have access to this protected route!"}
