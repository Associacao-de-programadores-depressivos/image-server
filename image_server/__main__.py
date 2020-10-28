import logging
import asyncio

from tortoise import run_async
from aiohttp import web
from dotenv import load_dotenv
from image_server.routes import add_routes_to_app
from . import load_model_in_app, init_database, close_database, init_firebase

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

app = web.Application()
app.on_startup.append(init_database)
app.on_startup.append(init_firebase)
app.on_shutdown.append(close_database)

add_routes_to_app(app)
load_model_in_app(app)

web.run_app(app, port=8081)
