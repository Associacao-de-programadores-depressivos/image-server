import numpy as np
import tensorflow as tf
import uuid
import json

from tortoise.models import Model
from tortoise import fields
from PIL import Image

from object_detection.utils import ops as utils_ops
from object_detection.utils import visualization_utils as vis_util

class ObjectDetection(Model):
    id = fields.CharField(pk=True, max_length=255)
    raw_image_url = fields.CharField(default=None, max_length=255)
    boundary_box_image_url = fields.CharField(default=None, max_length=255)
    detections = fields.JSONField(encoder=json.dumps, decoder=json.loads, default={})
    created_date = fields.DatetimeField(auto_now=True)

    @staticmethod
    def run_inference_for_single_image(model, np_img):
        input_tensor = tf.convert_to_tensor(np_img)
        input_tensor = input_tensor[tf.newaxis, ...]

        output_dict = model(input_tensor)

        num_detections = int(output_dict.pop("num_detections"))
        output_dict = {
            key: value[0, :num_detections].numpy() for key, value in output_dict.items()
        }
        output_dict["num_detections"] = num_detections
        output_dict["detection_classes"] = output_dict["detection_classes"].astype(np.int64)

        if "detection_masks" in output_dict:
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
                output_dict["detection_masks"],
                output_dict["detection_boxes"],
                image.shape[0],
                image.shape[1],
            )
            detection_masks_reframed = tf.cast(detection_masks_reframed > 0.5, tf.uint8)
            output_dict["detection_masks_reframed"] = detection_masks_reframed.numpy()

        return output_dict