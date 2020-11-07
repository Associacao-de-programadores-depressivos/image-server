import os
import logging
import firebase_admin

from typing import List
from datetime import timedelta

from firebase_admin import messaging
from firebase_admin import credentials

from image_server.models.object_detection import ObjectDetection
from image_server.utils.json import dumps

logger = logging.getLogger(__name__)


class Firebase:
    def __init__(self):
        self.get_cred_from_environ()
        cred = credentials.Certificate(os.environ["GOOGLE_SERVICE_ACCOUNT_PATH"])
        self._firebase = firebase_admin.initialize_app(cred)

    def get_cred_from_environ(self):
        with open(os.environ["GOOGLE_SERVICE_ACCOUNT_PATH"], "w") as f:
            f.write(os.environ["GOOGLE_SERVICE_ACCOUNT_CRED"])

    def send_detection_notification(
        self, detection: ObjectDetection, tokens: List[str]
    ):
        brazil_timezone = detection.created_date - timedelta(hours=3)
        day_date = brazil_timezone.strftime("%d/%m/%Y")
        hour_date = brazil_timezone.strftime("%H:%M:%S")

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

        message = messaging.MulticastMessage(
            data={
                "id": str(detection.id),
                "raw_image_url": str(detection.raw_image_url),
                "boundary_box_image_url": str(detection.boundary_box_image_url),
                "created_date": str(brazil_timezone),
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
            },
            notification=notification,
            android=android_config,
            tokens=tokens,
        )

        messaging.send_multicast(message)
