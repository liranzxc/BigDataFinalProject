from baseClasses.consumer import Consumer
from models.song import Song
from services.config_service import ConfigService
from services.song_analyzer_service import SongAnalyzerService
from pyspark import SparkContext, SparkConf


def doWork(data):
    song_profiles = []
    for song_json in data:
        # analyzer song and get result
        song_profiles.append(song_analyzer.analyze(Song.from_json_to_song(song_json)))
    # save song_profiles on db mongo



if __name__ == "__main__":
    sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

    song_analyzer = SongAnalyzerService(sc)

    configService = ConfigService()
    config = configService.getConfig()
    BOOTSTRAP_SERVER = config["KAFKA_HOST"] + ":" + config["KAFKA_PORT"]
    worker = Consumer(BOOTSTRAP_SERVER, config["UPLOAD_TOPIC"])
    worker.startReceive(doWork)

    # lyrics = "Black is the night, metal we fight Power amps set to explode. Energy screams, magic and dreams Satan records the first note. We chime the bell, chaos and hell Metal for maniacs pure. Faster than steel, fortune on wheels Brain haemorrhage is the cure."
    # analyzer = SongAnalyzer(Song("Venom", "Black Metal", lyrics))
    # print(analyzer)
