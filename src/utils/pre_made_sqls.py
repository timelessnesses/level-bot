from datetime import datetime

import asyncpg

db: asyncpg.Pool = None


async def set_database(database: asyncpg.Pool):
    global db
    db = database


async def fetch_user(user_id: int):
    async with db.acquire() as conn:
        return await conn.fetchrow("SELECT * FROM user_ WHERE user_id = $1", user_id)


async def dump_exp(user_id: int, exp: int):
    async with db.acquire() as conn:
        await conn.execute(
            "UPDATE user_ SET experience = $1 WHERE user_id = $2", exp, user_id
        )


async def update_user_voicechat(user_id: int, when: datetime):
    async with db.acquire() as conn:
        await conn.execute(
            "UPDATE user SET when_in_voice_channel = $1 WHERE user_id = $2",
            when,
            user_id,
        )


async def execute(schema: str, *args):
    async with db.acquire() as conn:
        return await conn.execute(schema, *args)
