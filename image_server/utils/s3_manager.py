import boto3, os

from image_server import TMP_FOLDER


class S3Manager:

    def __init__(self, bucket):
        self.client = boto3.client(
            's3',
            aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
            aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY']
        )
        self.bucket_name = bucket


    def send_image_to_storage(self, buffer: bytes, file_name: str) -> str:
        self.client.put_object(
            ACL='public-read',
            Body=buffer,
            Bucket=self.bucket_name,
            Key=file_name
        )

        return file_name