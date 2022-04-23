import os

import aioredis

from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse

from mangum import Mangum

redis = aioredis.from_url(
        f"redis://localhost", 
        max_connections=100, 
        encoding="utf-8", 
        decode_responses=True
)

stage = os.environ.get('STAGE', None)
root_path = f"/{stage}" if stage else "/"

app = FastAPI(title="FastRedis", root_path=root_path) 

@app.get("/")
async def root():
    data = { "foo": await redis.incr("foo") }
    return JSONResponse(content=jsonable_encoder(data))


@app.get("/info")
async def info():
    data = await redis.info()
    return JSONResponse(content=jsonable_encoder(data))


handler = Mangum(app)

# uvicorn fast-redis:app --reload
