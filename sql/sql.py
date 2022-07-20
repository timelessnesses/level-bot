import typing

import asyncpg


class EasySQL:
    def __init__(self) -> None:
        self.db: asyncpg.Pool = None

    async def connect(self, **kwargs) -> typing.NoReturn:
        self.db = await asyncpg.create_pool(**kwargs)

    async def execute(self, query, *args) -> typing.NoReturn:
        async with self.db.acquire() as conn:
            await conn.execute(query, *args)

    async def fetch(self, query, *args) -> typing.Optional[dict]:
        async with self.db.acquire() as conn:
            return await conn.fetch(query, *args)

    async def close(self) -> None:
        await self.db.close()

    async def commit(self) -> None:
        await self.db.commit()

    async def rollback(self) -> None:
        await self.db.rollback()

    async def __aenter__(self) -> "EasySQL":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
