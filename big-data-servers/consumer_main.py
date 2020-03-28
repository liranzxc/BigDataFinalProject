import concurrent
from concurrent.futures import ThreadPoolExecutor

import numpy as np

from baseClasses.consumer import Consumer
from services.nrc_service import NRC
from services.config_service import ConfigService
from services.mongodb_service import MongoDbService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf, SparkFiles
from models.song_profile import Song
import sys
import os
import nltk
import threading
import pandas as pd
from nltk.stem import WordNetLemmatizer


def do_work(data, extra_data=None):
    sc = extra_data["spark_context"]
    analyzer = extra_data["song_analyzer"]
    print("Consumer {} received a new batch".format(extra_data["consumerNumber"]))
    rdd = sc.parallelize(data)
    rdd = rdd.map(lambda song_json: print(Song.from_json_to_song(song_json)))
    rdd = rdd.map(lambda song: analyzer.analyze(song))
    rdd = rdd.map(lambda profile: profile.to_mongodb_document_format())
    NRC(ConfigService()).get_emotions_association("fuck")
    # for song_json in data:
    #     # analyzer song and get result
    #     print("Consumer working on song")
    #     song = Song.from_json_to_song(song_json)
    #     analyze = extraData["song_analyzer"].analyze(song)
    #
    #     # print(analyze)
    #     song_profiles.append(analyze)

    # save song_profiles on db mongo
    #songs_profiles_json = rdd.collect()
    #print(songs_profiles_json)
    #x = extra_data["mongodb_service"].upload_song_profiles(songs_profiles_json)

    # print list of the _id values of the inserted documents:
    #print(x.inserted_ids)


def consumer_main_thread(num_consumers):
    import pandas
    import nltk
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
        sc.addPyFile("./services/nrc_service.py")
    sys.path.insert(0, SparkFiles.getRootDirectory())

    song_analyzer = SongAnalyzerService(nrc=NRC(config))

    # num_emotions = config.number_emotions
    BOOTSTRAP_SERVER = config.kafka_server_address
    worker = Consumer(BOOTSTRAP_SERVER, config.kafka_upload_topic)
    worker.start_receive(do_work, extra_data={"song_analyzer": song_analyzer,
                                              "mongodb_service": mongodb_service,
                                              "consumerNumber": num_consumers,
                                              "spark_context": sc})


if __name__ == "__main__":
    print('Downloading wordnet...')
    nltk.download('wordnet')
    print('Finish download wordnet.')
    NUMBER_OF_CONSUMER = int(os.getenv("NUMBER_OF_CONSUMER", 1))
    jobs = np.arange(0, NUMBER_OF_CONSUMER, 1)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        for number in executor.map(consumer_main_thread, jobs):
            print("consumer % finish".format(number))
