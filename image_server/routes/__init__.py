from aiohttp import web
from .esp32cam import routes as esp32cam_routes

import aiohttp_cors


def add_routes_to_app(app: web.Application):
    app.add_routes(esp32cam_routes)

    cors = aiohttp_cors.setup(
        app,
        defaults={
            "*": aiohttp_cors.ResourceOptions(
                allow_credentials=True, expose_headers="*", allow_headers="*",
            )
        },
    )

    for route in list(app.router.routes()):
        cors.add(route)
