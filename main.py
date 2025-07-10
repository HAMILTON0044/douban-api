from fastapi import FastAPI
from pydantic import BaseModel
from crawler import getdata, savedata
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from Dify backend!"}

class CrawlRequest(BaseModel):
    filename: str = "douban_top250.xls"

@app.post("/crawl_douban")
def crawl_douban(req: CrawlRequest):
    baseurl = "https://movie.douban.com/top250?start="
    datalist = getdata(baseurl)
    if not datalist:
        return {"status": "fail", "message": "没有抓取到数据"}
    savepath = os.path.join(os.getcwd(), req.filename)
    savedata(datalist, savepath)
    return {"status": "success", "file": req.filename}

