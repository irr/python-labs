import asyncio
import aioredis

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi import FastAPI

app = FastAPI(title="FastRedis")

redis = aioredis.from_url(
        f"redis://localhost", 
        max_connections=100, 
        encoding="utf-8", 
        decode_responses=True)

@app.get("/")
async def root():
    data = { "foo": await redis.incr("foo") }
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/info")
async def info():
    data = await redis.info()
    return JSONResponse(content=jsonable_encoder(data))

# uvicorn fast-redis-36:app --reload
