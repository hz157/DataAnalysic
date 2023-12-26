from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api.bilibili import router as BilibiliRouter
from api.qqmusic import router as QQMusicRouter
from api.neteasemusic import router as NetEaseMusicRouter
from api.user import router as UserRouter
from api.public import router as PublicRouter

app = FastAPI()
app.include_router(BilibiliRouter, prefix="/api/bilibili")
app.include_router(QQMusicRouter, prefix="/api/qq_music")
app.include_router(NetEaseMusicRouter, prefix="/api/netease_music")
app.include_router(UserRouter, prefix="/api/user")
app.include_router(PublicRouter, prefix="/api/public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源的跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头部
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
