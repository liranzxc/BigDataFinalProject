import concurrent
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from baseClasses.consumer import Consumer
from services.nrc_service import NRC
from services.config_service import ConfigService
from services.mongodb_service import MongoDbService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf, SparkFiles
import nltk
from models.song_profile import Song
import sys
import os
import threading


def do_work(data, extra_data=None):
    song_profiles = []
    print("Consumer received a new batch")
    for song_json in data:
        # analyzer song and get result
        song = Song.from_json_to_song(song_json)
        analyze = extra_data["song_analyzer"].analyze(song)
        print(extra_data["number_consumers"])
        print(analyze)
        song_profiles.append(analyze)

    # save song_profiles on db mongo
    songs_profile_jsons_array = list(map(lambda sp: sp.to_mongodb_document_format(), song_profiles))
    extra_data["mongodb_service"].upload_song_profiles(songs_profile_jsons_array)

    # print list of the _id values of the inserted documents:
    # print(x.inserted_ids)


def consumer_main_thread(number_consumers):
    config = ConfigService()
    mongodb_service = MongoDbService(config)

    MAX_MEMORY = str(os.getenv("MAX_MEMORY", "1g"))
    sc = SparkContext \
        .getOrCreate(SparkConf().set("spark.executor.memory", MAX_MEMORY)
                     .set("spark.driver.memory", MAX_MEMORY)
                     .set("spark.cores.max", int(os.getenv("MAX_CORES", 1)))
                     .set("spark.scheduler.allocation.file", "./fairscheduler.xml")
                     .setMaster(config.spark_local))
    if os.getenv("DOCKER", False):
        sc.addPyFile("./all.zip")
    sys.path.insert(0, SparkFiles.getRootDirectory())

    # passing spark context and NRC instance (emotion analyzer)
    song_analyzer = SongAnalyzerService(sc=sc, nrc=NRC(config))
    BOOTSTRAP_SERVER = config.kafka_server_address
    worker = Consumer(BOOTSTRAP_SERVER, config.kafka_upload_topic)
    worker.start_receive(do_work, extra_data={"song_analyzer": song_analyzer,
                                             "mongodb_service": mongodb_service,
                                             "number_consumers": number_consumers})


if __name__ == "__main__":
    print('Downloading wordnet...')
    nltk.download('wordnet')
    print('Finished downloading wordnet.')
    NUMBER_OF_CONSUMER = int(os.getenv("NUMBER_OF_CONSUMER", 1))
    jobs = np.arange(0, NUMBER_OF_CONSUMER, 1)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number in executor.map(consumer_main_thread, jobs):
            print("consumer % finish".format(number))