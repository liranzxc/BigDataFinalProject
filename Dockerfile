FROM ubuntu:latest

WORKDIR /opt/app


RUN cat /etc/os-release

RUN apt-get update && apt-get install
RUN apt-get install build-essential -y
RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:linuxuprising/java
RUN apt-get update
RUN apt install openjdk-8-jdk -y
RUN java -version
RUN update-alternatives --config java

ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64
RUN printenv


RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y python3.7

RUN python3.7 -V
RUN apt-get install -y python3.7-dev
RUN apt install -y python3-pip

ADD ./requirements.txt ./requirements.txt
RUN python3.7 -m pip install -r ./requirements.txt

RUN apt-get install zip -y

ENV PYSPARK_PYTHON python3.7
COPY . /opt/app

RUN zip -r all.zip .

RUN ls -l