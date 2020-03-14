from baseClasses.producer import Producer
from services.config_service import ConfigService
from services.csv_service import CsvService

# producer main

if __name__ == "__main__":
    # read config file
    configService = ConfigService()
    config = configService.getConfig()

    # load csv
    df_songs, headers, songs_json = CsvService().read_csv()

    # upload songs via producer
    BOOTSTRAP_SERVER = config["KAFKA_HOST"] + ":" + config["KAFKA_PORT"]
    producer = Producer(BOOTSTRAP_SERVER, config["UPLOAD_TOPIC"])

    batchSize = config["BATCH_SIZE"]
    for i in range(0, len(songs_json), batchSize):
        batch = songs_json[i:i + batchSize]  # the result might be shorter than batchsize at the end
        future = producer.send(batch)
        result = future.get(timeout=0.5)
        print(result)
        print("producer send batch {} ~ {}".format(i, i + batchSize))

    print("producer finish send jobs")
