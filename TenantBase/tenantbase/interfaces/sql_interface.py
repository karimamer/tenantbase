import aiosqlite
import asyncio

DB = "tbase_cache.db"


async def get_value_from_sql(k):
    if k:
        given_key = (k,)
        async with aiosqlite.connect(DB) as db:
            cursor = await db.execute("select value from kvalue where key=?", given_key)
            rows = await cursor.fetchall()
            print(rows)
            return rows


async def delete_value_from_sql(k):
    if k:
        given_key = (k,)
        async with aiosqlite.connect(DB) as db:
            cursor = await db.cursor()
            await cursor.execute("Delete from kvalue where key=?", given_key)
            await db.commit()


async def insert_value_into_sql(k, v):
    if k and v:
        given_key_value = (k, v)

        async with aiosqlite.connect(DB) as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    "insert into kvalue( key , value) values (?,? )", given_key_value
                )
                await db.commit()
