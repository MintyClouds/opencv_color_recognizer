import redis

def get_redis() -> redis.client.Redis:
    redis_client = redis.Redis(
        host='redis',
        port=6379,
        db=0,
        decode_responses=True
    )
    return redis_client