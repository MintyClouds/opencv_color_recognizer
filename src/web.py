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
    res = {}
    keys = ['snake', 'ceiling_inner', 'ceiling_outer']
    for k in keys:
        value = redis_client.get(k)
        if isinstance(value, str):
            value = int(value)
        else:
            value = False

        res[k] = True if int(value) == 1 else False

    res['ceiling_full'] = res.get('ceiling_inner') and res.get('ceiling_outer')

    return LightsResponse(**res)
