from baseClasses.consumer import Consumer
from models.song import Song
from services.config_service import ConfigService
from services.mongodb_service import MongoDbService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf
import json

# TODO need to with spark
def doWork(data):
    song_profiles = []
    for song_json in data:
        # analyzer song and get result
        song_profiles.append(song_analyzer.analyze(Song.from_json_to_song(song_json)))

    # save song_profiles on db mongo
    songs_profile_jsons_array = list(map(lambda sp: sp.to_mongodb_document_format(), song_profiles))
    print(mongodb_service.upload_song_profiles(songs_profile_jsons_array))


if __name__ == "__main__":
    sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

    configService = ConfigService()
    config = configService.getConfig()

    song_analyzer = SongAnalyzerService(sc)
    mongodb_service = MongoDbService(config)

    BOOTSTRAP_SERVER = config["KAFKA_HOST"] + ":" + config["KAFKA_PORT"]
    worker = Consumer(BOOTSTRAP_SERVER, config["UPLOAD_TOPIC"])
    worker.startReceive(doWork)

    # lyrics = "Black is the night, metal we fight Power amps set to explode. Energy screams, magic and dreams Satan records the first note. We chime the bell, chaos and hell Metal for maniacs pure. Faster than steel, fortune on wheels Brain haemorrhage is the cure."
    # analyzer = SongAnalyzer(Song("Venom", "Black Metal", lyrics))
    # print(analyzer)
