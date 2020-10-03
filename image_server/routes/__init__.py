from aiohttp import web
from .esp32cam import routes as esp32cam_routes


def add_routes_to_app(app: web.Application):
    app.add_routes(esp32cam_routes)
