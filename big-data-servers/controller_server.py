import os
import threading

from flask import Flask, request
from flask_cors import cross_origin

from baseClasses.producer import Producer
from services.config_service import ConfigService
from services.csv_service import CsvService
from services.mongodb_service import MongoDbService
from bson.json_util import dumps

app = Flask(__name__)
import subprocess


def uploadProducerDocker():
    p = subprocess.call("docker-compose up producer -d", shell=True)
    print(p)


def updateConsumer():
    p = subprocess.call("docker-compose up producer -d", shell=True)
    print(p)


# delete db data
@app.route("/mongodb", methods=["DELETE"])
def deleteAllMongodb():
    mongodb_service.delete_all_records()
    return dumps({"message": "db deleted", "status": 200})


@app.route("/mongodb", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'Access-Control-Allow-Origin'])
def getAllRecords():
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 5))
    records = mongodb_service.get_all_records(page=page, size=size)
    return dumps(records)


@app.route("/mongodb/count", methods=["GET"])
def getCount():
    count = mongodb_service.get_counts()
    return dumps({"total": count})


@app.route("/producer", methods=["POST"])
def startProducer():
    x = threading.Thread(target=uploadProducerDocker)
    x.start()
    return dumps({"message": "producer started", "status": 200})


if __name__ == '__main__':
    config = ConfigService()
    mongodb_service = MongoDbService(config)
    app.run(host="0.0.0.0")
