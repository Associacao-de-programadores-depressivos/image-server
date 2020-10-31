import numpy as np
import logging
import time
import json
import os
import io
import asyncio

from aiohttp import web
from io import BytesIO
from os import path
from PIL import Image
from uuid import uuid4

from image_server.models.object_detection import ObjectDetection
from image_server.models.firebase_token import FirebaseToken
from object_detection.utils import visualization_utils as vis_util
from image_server.utils.json import dumps
from image_server.utils.s3_manager import S3Manager
from image_server.utils.firebase import Firebase

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)


@routes.get("/")
async def main(req: web.Request):
    return web.Response(text="Image Server is running!")


@routes.post("/mobile/register_firebase_token")
async def register_firebase_token(req: web.Request):
    if not req.has_body:
        return web.HTTPBadRequest(text="Invalid body")

    try:
        body = await req.json()
    except BaseException:
        msg = "Error decoding json"

        logger.exception(msg, exc_info=True)
        return web.HTTPInternalServerError(text=msg)

    if "device_id" not in body or "token" not in body:
        return web.HTTPBadRequest(text="Invalid body")

    try:
        device = await FirebaseToken.filter(device_id=body["device_id"]).first()

        if device:
            device.token = body["token"]
            await device.save()
        else:
            await FirebaseToken.create(**body)
    except BaseException:
        msg = "Error creating or updating token for device"

        logger.exception(msg, exc_info=True)
        return web.HTTPInternalServerError(text=msg)

    return web.Response(status=200)


@routes.get("/esp32cam/detections")
async def get_detections(req: web.Request):
    detections = []

    if "page" in req.query:
        page = int(req.query["page"])
        results = page * 10
        detections = (
            await ObjectDetection.all()
            .order_by("-created_date")
            .offset(results)
            .limit(10)
            .values()
        )
    else:
        detections = await ObjectDetection.all().order_by("-created_date").values()

    return web.json_response(detections, status=200, dumps=dumps)


@routes.post("/esp32cam/upload")
async def image(req: web.Request):
    try:
        post = await req.post()
        firebase: Firebase = req.app["firebase"]
        image = post.get("image")
        detections_limit = 5
        response = {"detections": []}
        s3 = S3Manager(os.environ["STORAGE_BUCKET_NAME"])

        if image:
            file_name = str(int(time.time())) + ".jpeg"
            img_content = image.file.read()
            buffer = BytesIO(img_content)
            np_img = np.array(Image.open(buffer))

            detections = ObjectDetection.run_inference_for_single_image(
                req.app["tf_model"], np_img
            )
            category_index = req.app["tf_category_index"]

            if "detection_scores" in detections and "detection_classes" in detections:
                classes = detections["detection_classes"].tolist()
                scores = detections["detection_scores"].tolist()

                for i, _class in enumerate(classes):
                    if detections_limit > 0:
                        if category_index[_class]["name"] == "person":
                            response["detections"].append(
                                {
                                    "object": category_index[_class]["name"],
                                    "score": scores[i],
                                }
                            )
                            detections_limit -= 1
                    else:
                        break

                if not response["detections"]:
                    return web.Response(status=200)

                s3.send_image_to_storage(img_content, file_name)

                vis_util.visualize_boxes_and_labels_on_image_array(
                    np_img,
                    detections["detection_boxes"],
                    detections["detection_classes"],
                    detections["detection_scores"],
                    category_index,
                    instance_masks=detections.get("detection_masks_reframed", None),
                    use_normalized_coordinates=True,
                    line_thickness=8,
                )

                boundary_box_file_name = "boundary_box/" + file_name
                img_bytes = io.BytesIO()
                img = Image.fromarray(np_img)
                img.save(img_bytes, format="JPEG")
                s3.send_image_to_storage(img_bytes.getvalue(), boundary_box_file_name)

                detection = await ObjectDetection.create(
                    id=str(uuid4()),
                    raw_image_url=os.environ["STORAGE_URL"] + file_name,
                    boundary_box_image_url=os.environ["STORAGE_URL"]
                    + "boundary_box/"
                    + file_name,
                    detections=response,
                )

                tokens = await FirebaseToken.all().values_list("token", flat=True)

                firebase.send_detection_notification(
                    detection,
                    tokens,
                )

            return web.Response(status=200)
        else:
            return web.HTTPBadRequest(text="An invalid or null image was received")
    except BaseException as e:
        logger.exception("An error occurred when processing image", exc_info=True)
        return web.HTTPInternalServerError()
