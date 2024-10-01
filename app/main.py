import logging

import redis.asyncio as redis
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from app import config
from app.routers.flight_router import router as flight_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger(__name__)


app = FastAPI()
app.include_router(flight_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    redis_client = redis.from_url(config.REDIS_URL, encoding="utf8")
    FastAPICache.init(RedisBackend(redis_client), prefix="flight_cache")


@app.on_event("shutdown")
async def shutdown():
    await FastAPICache.clear()
