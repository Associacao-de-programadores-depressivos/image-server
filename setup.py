from setuptools import find_packages, setup

setup(
    name="image_server",
    version="0.0.1",
    description="Simple API that handle ESP32 CAM requests",
    packages=find_packages(),
    install_requires=[
        # Firebase admin downloads an old version of requests, and it is broking the project
        # in order to fix that, we need to download the newest version of requests before firebase-admin
        "requests==2.24.0",
        "aiohttp==3.6.2",
        "Pillow==7.2.0",
        "numpy==1.18.5",
        "tf-slim==1.1.0",
        "tensorflow==2.3.1",
        "pycocotools==2.0.2",
        "aiomysql==0.0.20",
        "tortoise-orm==0.16.16",
        "python-dotenv==0.14.0",
        "aiohttp-cors==0.7.0",
        "boto3==1.13.5",
        "firebase-admin==4.4.0",
    ],
)
