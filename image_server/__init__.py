import os
import pathlib
import tensorflow as tf

from aiohttp.web import Application
from typing import Optional
from object_detection.utils import label_map_util
from tortoise import Tortoise

from image_server.models.object_detection import ObjectDetection
from image_server.utils.firebase import Firebase


TMP_FOLDER = "tmp"
PATH_TO_LABELS = "tf/research/object_detection/data/mscoco_label_map.pbtxt"


def create_tmp_folder() -> None:
    if TMP_FOLDER not in os.listdir():
        os.mkdir(TMP_FOLDER)


def load_model_in_app(app) -> None:
    model_name = "ssd_mobilenet_v1_coco_2017_11_17"
    base_url = "http://download.tensorflow.org/models/object_detection/"
    model_file = model_name + ".tar.gz"
    model_dir = tf.keras.utils.get_file(
        fname=model_name, origin=base_url + model_file, untar=True
    )

    model_dir = pathlib.Path(model_dir) / "saved_model"

    model = tf.saved_model.load(str(model_dir))
    model = model.signatures["serving_default"]

    app["tf_model"] = model

    category_index = label_map_util.create_category_index_from_labelmap(
        PATH_TO_LABELS, use_display_name=True
    )
    app["tf_category_index"] = category_index


async def init_database(app: Optional[Application]) -> None:
    await Tortoise.init(
        {
            "connections": {
                "default": f"mysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
            },
            "apps": {"models": {"models": ["image_server.models.object_detection"]}},
        }
    )
    await Tortoise.generate_schemas()


async def init_firebase(app: Optional[Application]) -> None:
    app["firebase"] = Firebase()


async def close_database(app: Optional[Application]) -> None:
    await Tortoise.close_connections()
