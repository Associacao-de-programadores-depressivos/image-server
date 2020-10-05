import logging

from aiohttp import web
from image_server.routes import add_routes_to_app
from image_server import create_tmp_folder

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = web.Application()

create_tmp_folder()
add_routes_to_app(app)

web.run_app(app, port=8081)
