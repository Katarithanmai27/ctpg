import asyncio
import time
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, HttpUrl

from src.crawler import WebCrawler
from src.async_crawler import AsyncWebCrawler

app = FastAPI(title="Intelligent Web Crawler")

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_DIR = BASE_DIR / "static"

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


class CrawlRequest(BaseModel):
    urls: list[HttpUrl]


@app.get("/")
def home():
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/api/crawl")
async def crawl(request: CrawlRequest):
    urls = [str(url) for url in request.urls]

    sequential = WebCrawler()
    start = time.perf_counter()
    sequential_results = await asyncio.to_thread(
        sequential.crawl_multiple, urls
    )
    sequential_time = time.perf_counter() - start

    asynchronous = AsyncWebCrawler()
    start = time.perf_counter()
    async_results = await asynchronous.crawl_multiple(urls)
    async_time = time.perf_counter() - start

    return {
        "sequential_time": round(sequential_time, 3),
        "async_time": round(async_time, 3),
        "sequential_results": sequential_results,
        "async_results": async_results,
    }
