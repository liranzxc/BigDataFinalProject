from baseClasses.producer import Producer
from services.config_service import ConfigService
from services.csv_service import CsvService
import logging
# producer main

if __name__ == "__main__":
    # read config file
    config = ConfigService()
    # load csv
    df_songs, headers, songs_json = CsvService().read_csv(config.song_lyrics_csv)

    # upload songs via producer
    producer = Producer(config.kafka_server_address, config.kafka_upload_topic)

    batchSize = int(config.batch_size)

    for i in range(0, len(songs_json), batchSize):
        batch = songs_json[i:i + batchSize]  # the result might be shorter than batchsize at the end
        future = producer.send(batch)
        result = future.get(timeout=config.send_batch_timeout)
        print(result)
        print("producer send batch {} ~ {}".format(i, i + batchSize))

    print("producer finish send jobs")
