import os
import logging
import firebase_admin

from firebase_admin import messaging
from firebase_admin import credentials

from image_server.models.object_detection import ObjectDetection
from image_server.utils.json import dumps

logger = logging.getLogger(__name__)


class Firebase:
    def __init__(self):
        cred = credentials.Certificate(os.environ["GOOGLE_SERVICE_ACCOUNT_PATH"])
        self._firebase = firebase_admin.initialize_app(cred)

    def send_detection_notification(self, detection: ObjectDetection, token: str):
        day_date = detection.created_date.strftime("%d/%m/%Y")
        hour_date = detection.created_date.strftime("%H:%M:%S")

        notification = messaging.Notification(
            "Nova detecção",
            f"Pessoa detectada em {day_date} às {hour_date}",
            detection.raw_image_url,
        )
        android_notification = messaging.AndroidNotification(
            click_action="FLUTTER_NOTIFICATION_CLICK",
            priority="high",
        )
        android_config = messaging.AndroidConfig(
            priority="high",
            notification=android_notification,
        )

        message = messaging.Message(
            data={
                "id": str(detection.id),
                "raw_image_url": str(detection.raw_image_url),
                "boundary_box_image_url": str(detection.boundary_box_image_url),
                "created_date": str(detection.created_date),
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                # "detections": dumps(detection.detections),
            },
            notification=notification,
            android=android_config,
            token=token,
        )

        messaging.send(message)
