FROM python:3.5.9-alpine3.10

RUN apk add build-base gcc abuild binutils binutils-doc gcc-doc bash bash-doc bash-completion openjdk8
WORKDIR /opt/app

RUN pip install --upgrade pip
COPY . /opt/app
RUN pip install -r requirements.txt
RUN python nltk_download.py
