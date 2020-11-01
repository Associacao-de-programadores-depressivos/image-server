FROM python:3.8.6-buster

EXPOSE 8081

ARG AWS_ACCESS_KEY_ID=""
ENV AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID

ARG AWS_SECRET_ACCESS_KEY=""
ENV AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY

ARG STORAGE_BUCKET_NAME=""
ENV STORAGE_BUCKET_NAME=$STORAGE_BUCKET_NAME

ARG STORAGE_URL=""
ENV STORAGE_URL=$STORAGE_URL

ARG GOOGLE_SERVICE_ACCOUNT_PATH="/usr/src/app/smart-eye-cred.json"
ENV GOOGLE_SERVICE_ACCOUNT_PATH=$GOOGLE_SERVICE_ACCOUNT_PATH

ARG DB_HOST="localhost"
ENV DB_HOST=$DB_HOST

ARG DB_PORT="3306"
ENV DB_PORT=$DB_PORT

ARG DB_USER="root"
ENV DB_USER=$DB_USER

ARG DB_PASSWORD="admin123"
ENV DB_PASSWORD=$DB_PASSWORD

ARG DB_NAME="smart_eye"
ENV DB_NAME=$DB_NAME

RUN apt-get update

RUN apt-get install -y protobuf-compiler

COPY . /usr/src/app

WORKDIR /usr/src/app/tf

RUN protoc object_detection/protos/*.proto --python_out=.

RUN python setup.py install

WORKDIR /usr/src/app

RUN echo "$GOOGLE_SERVICE_ACCOUNT_CRED" > "$GOOGLE_SERVICE_ACCOUNT_PATH"

ENTRYPOINT [ "./run.sh" ]