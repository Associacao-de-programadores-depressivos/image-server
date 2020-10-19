import numpy as np
import logging
import time
import json
import os

from aiohttp import web
from io import BytesIO
from os import path
from PIL import Image
from uuid import uuid4

from image_server.models.object_detection import ObjectDetection
from object_detection.utils import visualization_utils as vis_util
from image_server import TMP_FOLDER
from image_server.utils.json import dumps

routes = web.RouteTableDef()
logger = logging.getLogger(__name__)

routes.static("/image", os.getcwd() + "/tmp")

@routes.get("/")
async def main(req: web.Request):
    return web.Response(text="Image Server is running!")


@routes.get("/esp32cam/detections")
async def get_detections(req: web.Request):
    detections = await ObjectDetection.all().order_by("-created_date").values()
    return web.json_response(detections, status=200, dumps=dumps)


@routes.post("/esp32cam/upload")
async def image(req: web.Request):
    try:
        post = await req.post()
        image = post.get("image")
        detections_limit = 10
        response = {"detections": []}

        if image:
            file_name = str(int(time.time())) + ".jpeg"
            image_path = path.join(TMP_FOLDER, file_name)
            img_content = image.file.read()
            buffer = BytesIO(img_content)
            img = Image.open(buffer)
            img.save(image_path, "JPEG")

            detections = ObjectDetection.run_inference_for_single_image(req.app["tf_model"], image_path)
            category_index = req.app["tf_category_index"]

            if "detection_scores" in detections and "detection_classes" in detections:
                classes = detections["detection_classes"].tolist()
                scores = detections["detection_scores"].tolist()
                
                for i, _class in enumerate(classes):
                    if detections_limit > 0:
                        response["detections"].append({
                            "object": category_index[_class]["name"],
                            "score": scores[i]
                        })
                        detections_limit -= 1
                    else:
                        break
                
                image_np = np.array(Image.open(image_path))
                vis_util.visualize_boxes_and_labels_on_image_array(
                    image_np,
                    detections["detection_boxes"],
                    detections["detection_classes"],
                    detections["detection_scores"],
                    category_index,
                    instance_masks=detections.get("detection_masks_reframed", None),
                    use_normalized_coordinates=True,
                    line_thickness=8,
                )

                boundary_box_file_name = TMP_FOLDER + "/boundary_box/" + file_name
                img = Image.fromarray(image_np)
                img.save(boundary_box_file_name)

                await ObjectDetection.create(
                    id=str(uuid4()),
                    raw_image_url="http://localhost:8081/image/" + file_name,
                    boundary_box_image_url="http://localhost:8081/image/boundary_box/" + file_name,
                    detections=response,
                )

            return web.Response(status=200)
        else:
            return web.HTTPBadRequest(text="An invalid or null image was received")
    except Exception as e:
        logger.exception("An error occurred when processing image", exc_info=True)
        return web.HTTPInternalServerError()
