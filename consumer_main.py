from baseClasses.consumer import Consumer
from services.config_service import ConfigService


def doWork(data):
    print(data)


if __name__ == "__main__":
    configService = ConfigService()
    config = configService.getConfig()

    BOOTSTRAP_SERVER = config["KAFKA_HOST"] + ":" + config["KAFKA_PORT"]
    worker = Consumer(BOOTSTRAP_SERVER, config["UPLOAD_TOPIC"])

    worker.startReceive(doWork)

    # lyrics = "Black is the night, metal we fight Power amps set to explode. Energy screams, magic and dreams Satan records the first note. We chime the bell, chaos and hell Metal for maniacs pure. Faster than steel, fortune on wheels Brain haemorrhage is the cure."
    # analyzer = SongAnalyzer(Song("Venom", "Black Metal", lyrics))
    # print(analyzer)
