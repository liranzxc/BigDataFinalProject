import os


class ConfigService:
    def __init__(self):

        self.kafka_host = os.getenv("KAFKA_HOST", "localhost")
        self.kafka_port = os.getenv("KAFKA_PORT", "9092")
        self.kafka_upload_topic = os.getenv("UPLOAD_TOPIC", "test26")
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
        self.batch_size = os.getenv("BATCH_SIZE", 5)
        self.send_batch_timeout = 40
        self.spark_local = os.getenv("SPARK_LOCAL", "local[*]")
        self.spark_emolex_format = "com.databricks.spark.csv"
        self.song_lyrics_csv = "datasets/songdata.csv"
        self.emotion_lex_path = os.getenv("NRC_EMOTION_LEX", "datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt")
        self.spark_scheduler = "./fairscheduler.xml"
        self.kafka_server_address = self.kafka_host + ":" + self.kafka_port
        self.mongodb_address = "mongodb://" + self.mongodb_host + ":" + self.mongodb_port + "/"
