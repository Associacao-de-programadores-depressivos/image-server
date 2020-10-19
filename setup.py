from setuptools import find_packages, setup

setup(
    name="image_server",
    version="0.0.1",
    description="Simple API that handle ESP32 CAM requests",
    packages=find_packages(),
    install_requires=[
        "aiohttp==3.6.2",
        "Pillow==7.2.0",
        "gitdb==4.0.5",
        "gitpython==0.3.6",
        "numpy==1.18.5",
        "tensorflow==2.3.1",
        "pycocotools==2.0.2",
        "aiomysql==0.0.20",
        "tortoise-orm==0.16.16",
        "python-dotenv==0.14.0",
        "aiohttp-cors==0.7.0",
    ],
)
