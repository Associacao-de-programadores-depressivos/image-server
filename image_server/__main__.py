import logging
import asyncio

from tortoise import run_async
from aiohttp import web
from image_server.routes import add_routes_to_app
from image_server import create_tmp_folder
from . import load_model_in_app, init_database, close_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = web.Application()
app.on_startup.append(init_database)
app.on_shutdown.append(close_database)

create_tmp_folder()
add_routes_to_app(app)
load_model_in_app(app)

web.run_app(app, port=8081)
