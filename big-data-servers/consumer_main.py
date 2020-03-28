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


def do_work(data, extraData=None):
    sc = extraData["spark_context"]
    analyzer = extraData["song_analyzer"]
    print("Consumer {} received a new batch".format(extraData["consumerNumber"]))
    songs_rdd = sc.parallelize(data).map(lambda song_json: Song.from_json_to_song(song_json))\
        .map(lambda song: analyzer.analyze(song).to_mongodb_document_format())

    # for song_json in data:
    #     # analyzer song and get result
    #     print("Consumer working on song")
    #     song = Song.from_json_to_song(song_json)
    #     analyze = extraData["song_analyzer"].analyze(song)
    #
    #     # print(analyze)
    #     song_profiles.append(analyze)

    # save song_profiles on db mongo
    songs_profiles = songs_rdd.collect()
    print(songs_profiles)
    #x = extraData["mongodb_service"].upload_song_profiles(songs_profile_jsons_array)

    # print list of the _id values of the inserted documents:
    print(x.inserted_ids)


def consumer_main_thread(consumerNumber):
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
    song_analyzer = SongAnalyzerService(NRC(config))

    # num_emotions = config.number_emotions
    BOOTSTRAP_SERVER = config.kafka_server_address
    worker = Consumer(BOOTSTRAP_SERVER, config.kafka_upload_topic)
    worker.start_receive(do_work, extraData={"song_analyzer": song_analyzer,
                                             "mongodb_service": mongodb_service,
                                             "consumerNumber": consumerNumber,
                                             "spark_context": sc})


if __name__ == "__main__":
    print('downloading wordnet...')
    nltk.download('wordnet')
    print('finish download wordnet.')
    NUMBER_OF_CONSUMER = int(os.getenv("NUMBER_OF_CONSUMER", 1))
    jobs = np.arange(0, NUMBER_OF_CONSUMER, 1)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number in executor.map(consumer_main_thread, jobs):
            print("consumer % finish".format(number))
