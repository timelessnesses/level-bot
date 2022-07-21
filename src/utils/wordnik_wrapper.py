import aiohttp
from dotenv import load_dotenv

load_dotenv()
import os


async def get_random_word():
    async with aiohttp.ClientSession() as session:
        keys = os.getenv("WORDNIK_API_KEY").split(",")
        for api_key in keys:
            async with session.get(
                "https://api.wordnik.com/v4/words.json/randomWord?hasDictionaryDef=true&maxCorpusCount=-1&minDictionaryCount=1&maxDictionaryCount=-1&minLength=0&maxLength=-1&api_key={}".format(
                    api_key
                )
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    continue
                if data["word"]:
                    return data["word"]
