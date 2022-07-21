import asyncio
import time
from datetime import timedelta

from src.utils.imagegen import Generator

for x in range(10):
    start = time.perf_counter()
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
    )
    print(timedelta(seconds=time.time() - start))
