# src/redis_client/client.py
import redis.asyncio as aioredis
from telebot.types import Message

from os import getenv
from dotenv import load_dotenv


load_dotenv()

redis_url = getenv("REDIS_URL")
print(redis_url)

redis = aioredis.from_url(
        redis_url,
        decode_responses = True
    )

async def authorize(token: str, message: Message)-> bool:
    async with redis.client() as conn:
        redis_token = await redis.hgetall(f'sync_tokens:{token}')
        print(redis_token)

        await redis.set(
            'tg_user_id', message.from_user.id,
            'chat_id', message.chat.id
        )

        redis_token = await redis.hgetall(f'sync_tokens:{token}')
        print(redis_token)

        if redis_token:
            return redis_token
        return None




