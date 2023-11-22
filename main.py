from fastapi import FastAPI
from api import data_api


app = FastAPI()
app.include_router(data_api, prefix="/data")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
