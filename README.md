# Image Server

Image Server is a handler for ESP32CAM requests, treating the image received and saving it on a storage service.

## Development environment

We use in our development environment [pyenv](https://github.com/pyenv/pyenv) with [virtualenv](https://github.com/pyenv/pyenv-virtualenv) extension to manage our python versions and environments. But feel free to use other tools to manage and install Python versions. Below there is a simple tutorial showing how to setup your environment with `pyenv`.

### Downloading Python 3.8.3

To install the python version that we use on the project, simply run the code below on your terminal:

    $ pyenv install 3.8.3

After the download is complete, you can check if the python version was downloaded successfully if the version 3.8.3 appears after running the following command:

    $ pyenv versions

### Creating a virtualenv

Now that you already have the python 3.8.3 installed, we are going to create a virtual environment for it, by running the following command:

    $ pyenv virtualenv 3.8.3 image-server

### Using the virtualenv

By default the project already have a `.python-version` file that will automatically change your version, if you are using VS Code. But if you are using another IDE to run and execute your code, you can activate your environment by just using the following command:

    $ pyenv activate image-server

To check if you are running the correct python version, run on your terminal:

    $ python --version