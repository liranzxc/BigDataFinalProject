import os
import threading

from flask import Flask, request
from baseClasses.producer import Producer
from services.config_service import ConfigService
from services.csv_service import CsvService
from services.mongodb_service import MongoDbService
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

import subprocess
import enum

DOCKER_COMPOSE_CONSUMER = 'docker-compose-consumer.yml'
DOCKER_COMPOSE_PRODUCER = 'docker-compose-producer.yml'

consumer_state = False


class OperateDocker(enum.Enum):
    UP = "up"
    DOWN = "down"


def docker_compose_operation(docker_compose_name_file=None, operation=OperateDocker.UP):
    if docker_compose_name_file is None:
        print("docker-compose {} -d".format(operation.value))
        if operation.value is OperateDocker.DOWN.value:
            p = subprocess.call("docker-compose {}".format(operation.value), shell=True)
        else:
            p = subprocess.call("docker-compose {} -d".format(operation.value), shell=True)
        print(p)
    else:
        if operation.value is OperateDocker.DOWN.value:
            print("docker-compose --file {} {}".format(docker_compose_name_file, operation.value))
            p = subprocess.call("docker-compose --file {} {}".format(docker_compose_name_file, operation.value),
                                shell=True)
        else:
            print("docker-compose --file {} {} -d".format(docker_compose_name_file, operation.value))
            p = subprocess.call("docker-compose --file {} {} -d".format(docker_compose_name_file, operation.value),
                                shell=True)
        print(p)


@app.route("/stopConsumer", methods=["GET"])
def stopConsumer():
    # shut down docker compose consumer
    global consumer_state
    docker_compose_operation(docker_compose_name_file=DOCKER_COMPOSE_CONSUMER, operation=OperateDocker.DOWN)
    consumer_state = False
    print("here")
    return dumps({"message": "consumer down", "status": 200})


@app.route("/consumerState", methods=["GET"])
def consumerStatus():
    return dumps({"state": consumer_state, "status": 200})


# delete db data
@app.route("/mongodb", methods=["DELETE"])
@cross_origin(allow_headers=['Content-Type', 'Access-Control-Allow-Origin'])
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


@app.route("/mongodb/artist/<string:letter>", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'Access-Control-Allow-Origin'])
def getAllRecordsByArtistLetter(letter):
    page = int(request.args.get("page", 0))
    size = int(request.args.get("size", 5))
    records = mongodb_service.get_records_artist_by_letter(page=page, size=size, letter=letter)
    return dumps(records)


@app.route("/mongodb/count", methods=["GET"])
@cross_origin(allow_headers=['Content-Type', 'Access-Control-Allow-Origin'])
def getCount():
    count = mongodb_service.get_counts()
    return dumps({"total": count})


@app.route("/createEnv", methods=["POST"])
def createEnvConfig():
    global consumer_state
    json = request.json
    MAX_CORES = str(json["numOfCores"])
    MAX_MEMORY = str(json["memoryPerWorker"])
    NUMBER_OF_CONSUMER = str(json["numOfWorkers"])

    # create new config .env file
    text = "MAX_CORES=" + MAX_CORES + "\n" + "MAX_MEMORY=" + MAX_MEMORY + "\n" + "NUMBER_OF_CONSUMER=" + NUMBER_OF_CONSUMER
    with open(".env", "w") as file:
        file.write(text)

    # shut down docker compose consumer
    docker_compose_operation(docker_compose_name_file=DOCKER_COMPOSE_CONSUMER, operation=OperateDocker.DOWN)

    # up consumer again
    docker_compose_operation(docker_compose_name_file=DOCKER_COMPOSE_CONSUMER, operation=OperateDocker.UP)

    consumer_state = True
    return dumps({"message": "consumer recreate with new config file", "status": 200})


@app.route("/startProducer")
def startProducer():
    docker_compose_operation(docker_compose_name_file=DOCKER_COMPOSE_PRODUCER, operation=OperateDocker.UP)
    return dumps({"message": "producer up", "status": 200})


if __name__ == '__main__':
    config = ConfigService()
    mongodb_service = MongoDbService(config)
    # upload resource
    docker_compose_operation(None, operation=OperateDocker.UP)
    app.run(host="0.0.0.0")
