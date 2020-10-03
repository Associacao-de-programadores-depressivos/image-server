from setuptools import find_packages, setup

setup(
    name="image_server",
    version="0.0.1",
    description="Simple API that handle ESP32 CAM requests",
    packages=find_packages(),
    install_requires=["aiohttp==3.6.2",],
)
