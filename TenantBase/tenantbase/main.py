import asyncio
from functools import update_wrapper
import logging

import click
import aiohttp

from interfaces.memcache_interface import (
    set_memcahce,
    get_from_memcahce,
    delete_from_memcahce,
)
from interfaces.sql_interface import (
    get_value_from_sql,
    delete_value_from_sql,
    insert_value_into_sql,
)

# Globals
LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def coro(f):
    """
    a decerator to allow us to pass aysnc functions to click
    """
    f = asyncio.coroutine(f)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(f(*args, **kwargs))

    return update_wrapper(wrapper, f)


@click.group()
def entrypoint():
    """
    An entry poetry for the command line grouping
    """
    pass


@click.command()
@click.option("--key", prompt="Please enter your key")
@click.option("--value", prompt="Please enter your value")
@coro
def set_cache(key, value):
    set_memcahce(key, value)
    LOG.info(f"{key}{value} inserted in memchace")
    yield from insert_value_into_sql(key, value)
    LOG.info(f"{key}{value} inserted in sqlite")


@click.command()
@click.option("--key", prompt="Please enter your key")
@coro
def get_from_cache(key):
    cached_res = get_from_memcahce(key)
    if cached_res:
        print(cached_res)
        return cached_res
    else:
        res_from_sql = yield from get_value_from_sql(key)
        LOG.info(f"{key} found in sqlite")
        return res_from_sql


@click.command()
@click.option("--key", prompt="Please enter your key")
@coro
def delete_from_cache(key):
    delete_from_memcahce(key)
    res_from_sql = yield from delete_value_from_sql(key)
    LOG.info(f"{key} deleted in memchace and sqlite")
    return res_from_sql


entrypoint.add_command(delete_from_cache)
entrypoint.add_command(get_from_cache)
entrypoint.add_command(set_cache)

if __name__ == "__main__":
    entrypoint()
