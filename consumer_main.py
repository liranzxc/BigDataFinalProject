from baseClasses.consumer import Consumer
from models.song import Song
from nrc.read_nrc_database import NRC
from services.config_service import ConfigService
from services.mongodb_service import MongoDbService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf
import json
import nltk


#
# # TODO need to with spark
def do_work(data):
    song_profiles = []
    print("Consumer received a new batch")
    for song_json in data:
        # analyzer song and get result
        print("Consumer working on song")
        song = Song.from_json_to_song(song_json)
        analyze = song_analyzer.analyze(song, num_emotions=num_emotions)
        print(analyze)
        song_profiles.append(analyze)

    # save song_profiles on db mongo
    songs_profile_jsons_array = list(map(lambda sp: sp.to_mongodb_document_format(), song_profiles))
    print(mongodb_service.upload_song_profiles(songs_profile_jsons_array))


if __name__ == "__main__":
    print('downloading wordnet...')
    nltk.download('wordnet')
    print('finish download wordnet.')

    config = ConfigService()
    mongodb_service = MongoDbService(config)
    print("here after config")


    print("after sc started")
    sc = SparkContext.getOrCreate(SparkConf().setMaster(config.spark_local))
    song_analyzer = SongAnalyzerService(sc, NRC())

    num_emotions = config.number_emotions
    BOOTSTRAP_SERVER = config.kafka_server_address
    worker = Consumer(BOOTSTRAP_SERVER, config.kafka_upload_topic)
    worker.startReceive(do_work)
