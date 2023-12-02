from fastapi import FastAPI

from api.bilibili import router as BilibiliRouter
from api.qqmusic import router as QQMusicRouter
from api.neteasemusic import router as NetEaseMusicRouter

app = FastAPI()
app.include_router(BilibiliRouter, prefix="/bilibili")
app.include_router(QQMusicRouter, prefix="/qq_music")
app.include_router(NetEaseMusicRouter, prefix="/netease_music")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
