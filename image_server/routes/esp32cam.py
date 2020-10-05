from aiohttp import web
from io import BytesIO
from os import path
from PIL import Image

from image_server import TMP_FOLDER

import logging
import time

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)


@routes.get("/")
async def main(req: web.Request):
    return web.Response(text="Image Server is running!")


@routes.post("/esp32cam/upload")
async def image(req: web.Request):
    try:
        post = await req.post()
        image = post.get("image")

        if image:
            file_name = str(int(time.time())) + ".jpeg"
            img_content = image.file.read()
            buffer = BytesIO(img_content)
            img = Image.open(buffer)
            img.save(path.join(TMP_FOLDER, file_name), "JPEG")

            return web.Response(status=200)
        else:
            return web.HTTPBadRequest(text="An invalid or null image was received")
    except Exception as e:
        logger.exception("An error occurred when processing image", exc_info=True)
        return web.HTTPInternalServerError()
