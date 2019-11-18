import asyncio
from functools import update_wrapper

import click
import aiohttp

from interfaces.memecache_interface import (
    set_memecahce,
    get_from_memcahce,
    delete_from_memcahce,
)
from interfaces.sql_interface import (
    get_value_from_sql,
    delete_value_from_sql,
    insert_value_into_sql,
)


def coro(f):
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


@click.command()
@click.option("--key", prompt="Please enter your key")
@click.option("--value", prompt="Please enter your value")
@coro
def set_cache(key, value):
    set_memecahce(key, value)
    yield from insert_value_into_sql(key, value)


@click.command()
@click.option("--key", prompt="Please enter your key")
@coro
def get_from_cache(key):
    get_from_memcahce(key)
    res_from_sql = yield from get_value_from_sql(key)
    return res_from_sql


@click.command()
@click.option("--key", prompt="Please enter your key")
@coro
def delete_from_cache(key):
    delete_from_memcahce(key)
    res_from_sql = yield from delete_value_from_sql(key)
    return res_from_sql


if __name__ == "__main__":
    set_cache()
