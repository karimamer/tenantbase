import aiosqlite
import asyncio
import logging

# GLOBALS
DB = "tbase_cache.db"
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


async def get_value_from_sql(key):
    if key:
        given_key = (key,)
        async with aiosqlite.connect(DB) as db:
            cursor = await db.execute("select value from kvalue where key=?", given_key)
            rows = await cursor.fetchall()
            return rows
    else:
        LOG.info(f"{key} not found in sqlite")


async def delete_value_from_sql(key):
    if key:
        given_key = (key,)
        async with aiosqlite.connect(DB) as db:
            cursor = await db.cursor()
            await cursor.execute("Delete from kvalue where key=?", given_key)
            await db.commit()
    else:
        LOG.info(f"{key} not found in sqlite")


async def insert_value_into_sql(key, value):
    if key and value:
        given_key_value = (key, value)

        async with aiosqlite.connect(DB) as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    "insert into kvalue( key , value) values (?,? )", given_key_value
                )
                await db.commit()
    else:
        LOG.info(f"{key}{value} was not provided by user")
