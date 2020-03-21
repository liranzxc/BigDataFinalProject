FROM python:3.6.3

WORKDIR /opt/app
RUN apt-get update

RUN apt-get install openjdk-7-jdk -y
RUN apt-get install build-essential -y

RUN echo $JAVA_HOME

ADD ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r ./requirements.txt


ENV PYSPARK_PYTHON python3
COPY . /opt/app