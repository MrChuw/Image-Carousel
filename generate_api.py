import asyncio
import secrets

from tortoise import Tortoise

from schemas import APIKey


async def init():
    await Tortoise.init(db_url='sqlite://db.sqlite3', modules={'models': ['schemas']}
                        )
    await Tortoise.generate_schemas()


async def generate_api_key():
    key = secrets.token_hex(16)
    api_key = await APIKey.create(key=key)
    return api_key.key


async def main():
    await init()
    print(await generate_api_key())
    await Tortoise.close_connections()
    exit()


if __name__ == '__main__':
    asyncio.run(main())
