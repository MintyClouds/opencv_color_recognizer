from fastapi import FastAPI
from pydantic import BaseModel

from src.redis_utils import get_redis

app = FastAPI()
redis_client = get_redis()

class LightsResponse(BaseModel):
    snake: bool
    ceiling_inner: bool
    ceiling_outer: bool
    ceiling_full: bool


@app.get('/', response_model=LightsResponse)
async def get():

    snake = True if redis_client.get('snake') else False
    ceiling_inner = True if redis_client.get('ceiling_inner') else False
    ceiling_outer = True if redis_client.get('ceiling_outer') else False
    ceiling_full = ceiling_inner and ceiling_outer

    return LightsResponse(
        snake=snake,
        ceiling_inner=ceiling_inner,
        ceiling_outer=ceiling_outer,
        ceiling_full=ceiling_full
    )
