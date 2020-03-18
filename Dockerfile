FROM python:3.5.9-alpine3.10

RUN apk add build-base gcc abuild binutils binutils-doc gcc-doc bash bash-doc bash-completion openjdk8
WORKDIR /opt/app

ADD ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt


COPY . /opt/app
RUN python nltk_download.py
