import json
import os


class ConfigService:
    def __init__(self):
        self.kafka_host = os.getenv("KAFKA_HOST", "172.25.0.12")
        self.kafka_port = os.getenv("KAFKA_PORT", "9092")
        self.kafka_upload_topic = os.getenv("UPLOAD_TOPIC", "test8")
        self.mongodb_host = os.getenv("MONGODB_HOST", "localhost")
        self.mongodb_port = os.getenv("MONGODB_PORT", "27017")
        self.mongodb_db_name = os.getenv("MONGODB_DB_NAME", "songs")
        self.mongodb_result_collection = os.getenv("MONGODB_RESULT_COLLECTION", "result")
        self.mongodb_connection_timeout = 5000
        self.mongodb_socket_timeout = 5000
        self.mongodb_server_selection_timeout = 2000

        self.emolex_word_col = "word"
        self.emolex_association_col = "association"
        self.emolex_emotion_col = "emotion"
        self.emolex_delimiter = "\t"
        self.number_emotions = os.getenv("NUMBER_OF_EMOTIONS", 4)
        self.batch_size = os.getenv("BATCH_SIZE", 400)
        self.send_batch_timeout = 0.5
        self.spark_local = os.getenv("SPARK_LOCAL", "local[*]")
        self.spark_emolex_format = "com.databricks.spark.csv"
        self.song_json_artist = 'artist'
        self.song_json_lyrics = "text"
        self.song_json_name = "song_name"

        self.emotion_lex_path = os.getenv("NRC_EMOTION_LEX", "datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")

        self.kafka_server_address = self.kafka_host + ":" + self.kafka_port
        self.mongodb_address = "mongodb://" + self.mongodb_host + ":" + self.mongodb_port + "/"
