# src/redis_client/client.py
import asyncio
import redis.asyncio as aioredis

from os import getenv
from dotenv import load_dotenv


load_dotenv()

redis_url = getenv("REDIS_URL")
print(redis_url)



async def redis_connection():

    redis = aioredis.from_url(
        redis_url,
        decode_responses = True
    )


    async with redis.client() as conn:
        ok = await conn.execute_command("set", "my_key", "some_value")
        assert ok is True

        str_value = await conn.execute_command("get", "my_key")
        assert str_value == "some_value"
        print(str_value)

