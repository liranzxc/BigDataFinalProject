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

RUN ls -l /usr/bin/
RUN python3 -V
RUN apt install -y python3-pip

ADD ./requirements.txt ./requirements.txt
RUN pip3 install -r ./requirements.txt


ENV PYSPARK_PYTHON python3.6
COPY . /opt/app