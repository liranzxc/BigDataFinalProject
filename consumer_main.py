from baseClasses.consumer import Consumer
from services.nrc_service import NRC
from services.config_service import ConfigService
from services.mongodb_service import MongoDbService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf, SparkFiles
import nltk
from models.song_profile import Song
from glob import glob
import sys
import os


def do_work(data):
    song_profiles = []
    print("Consumer received a new batch")
    for song_json in data:
        # analyzer song and get result
        print("Consumer working on song")
        song = Song.from_json_to_song(song_json)
        analyze = song_analyzer.analyze(song)
        print(analyze)
        song_profiles.append(analyze)

    # save song_profiles on db mongo
    songs_profile_jsons_array = list(map(lambda sp: sp.to_mongodb_document_format(), song_profiles))
    x = mongodb_service.upload_song_profiles(songs_profile_jsons_array)

    # print list of the _id values of the inserted documents:
    print(x.inserted_ids)


if __name__ == "__main__":
    print('downloading wordnet...')
    nltk.download('wordnet')
    print('finish download wordnet.')

    config = ConfigService()
    mongodb_service = MongoDbService(config)
    print("here after config")
    MAX_MEMORY = "5g"
    print(config.spark_local)
    sc = SparkContext \
        .getOrCreate(SparkConf().set("spark.executor.memory", MAX_MEMORY) \
                     .set("spark.driver.memory", MAX_MEMORY).setMaster(config.spark_local))

    if os.getenv("DOCKER", False):
        sc.addPyFile("./all.zip")

    sys.path.insert(0, SparkFiles.getRootDirectory())

    print(sc.version)
    song_analyzer = SongAnalyzerService(sc, NRC(config))
    print("after sc started")

    num_emotions = config.number_emotions
    BOOTSTRAP_SERVER = config.kafka_server_address
    worker = Consumer(BOOTSTRAP_SERVER, config.kafka_upload_topic)
    worker.start_receive(do_work)
    # test work
    # songC = Song("liran artices", "lsdlkmsd", "hello world")
    #
    # song = SongProfile(song=songC, number_of_words=2424, histogram={"hello": 1}, emotion="hello")
    # song_profiles = [song.to_mongodb_document_format()]
    #
    # x = mongodb_service.upload_song_profiles(song_profiles)
    # # print list of the _id values of the inserted documents:
    # print(x.inserted_ids)
