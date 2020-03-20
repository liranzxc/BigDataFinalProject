FROM python:3.7-alpine3.10

RUN apk add --update alpine-sdk
WORKDIR /opt/app

ADD ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt


ENV PYSPARK_PYTHON python3
ENV PYTHON_DRIVER_SPARK python3
COPY . /opt/app