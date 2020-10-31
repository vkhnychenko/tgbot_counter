import asyncio
from typing import Optional

import aioredis

from data import config

redis: Optional[aioredis.Redis] = None


async def create_pools():
    global redis
    redis = await aioredis.create_redis_pool(config.REDIS_HOST)


asyncio.get_event_loop().run_until_complete(create_pools())
