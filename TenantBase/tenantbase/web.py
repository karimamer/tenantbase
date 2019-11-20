import json

import aiohttp
from aiohttp import web
import aiohttp_cors

from interfaces.memcache_interface import (
    set_memcahce,
    get_from_memcahce,
    delete_from_memcahce,
)
from interfaces.sql_interface import (
    get_value_from_sql,
    delete_value_from_sql,
    insert_value_into_sql,
    get_all_values,
)


async def health_check(request):
    return web.Response(text="servie is up and running")


async def get_value(request):
    try:
        key = await request.json()
        value_from_cache = get_from_memcahce(key["value"])
        data = {"value": value_from_cache}
        if value_from_cache is None:
            value = await get_value_from_sql(key["value"])
            data = {"value": value}
        return web.json_response(data)
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(text="You have not specified value") from e


async def set_value(request):
    try:
        data = await request.json()
        key = data["key"]
        value = data["value"]
        await insert_value_into_sql(key, value)
        set_memcahce(key, value)
        return web.HTTPOk()
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(text="You have not specified key and value") from e


async def delete_value(request):
    try:
        key = await request.json()
        delete_from_memcahce(key["value"])
        await delete_value_from_sql(key["value"])
        return web.HTTPNoContent()
    except (KeyError, TypeError, ValueError) as e:
        raise web.HTTPBadRequest(text="You have not specified value") from e


async def get_values(request):
    values = await get_all_values()
    data = {
        "value": [{"id": id, "key": key, "value": value} for id, key, value in values]
    }
    return web.json_response(data)


routes_list = [
    web.get("/health-check", health_check),
    web.get("/get-value", get_value),
    web.post("/set-value", set_value),
    web.delete("/delete-value", delete_value),
    web.get("/get-values", get_values),
]

app = web.Application()

app.add_routes(routes_list)


# Configure default CORS settings.
cors = aiohttp_cors.setup(
    app,
    defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True, expose_headers="*", allow_headers="*",
        )
    },
)

# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)

web.run_app(app)
