from aiohttp import web
from image_server.routes import add_routes_to_app

app = web.Application()

add_routes_to_app(app)

web.run_app(app, port=8081)
