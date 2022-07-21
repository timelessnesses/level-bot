import asyncio

from src.utils.imagegen import Generator

open("g.png", "wb").write(
    asyncio.run(
        Generator().generate_profile(
            None,
            "http://localhost/61a06af00bf7c9b332b5c134.jpg",
            69,
            420,
            1000,
            1,
            "deez nut#0000",
            "online",
        )
    ).fp.read()
)
