import json

# TODO change config architecture

class ConfigService:
    @staticmethod
    def get_configs(path_config: str = 'config/config.json'):
        with open(path_config) as json_file:
            data = json.load(json_file)
            return data

    config = get_configs.__func__()

    def __init__(self):

        self.kafka_host = ConfigService.config["KAFKA_HOST"]
        self.kafka_port = ConfigService.config["KAFKA_PORT"]

        self.kafka_upload_topic = ConfigService.config["UPLOAD_TOPIC"]

        self.mongodb_host = ConfigService.config["MONGODB_HOST"]
        self.mongodb_port = ConfigService.config["MONGODB_PORT"]
        self.mongodb_db_name = ConfigService.config["MONGODB_DB_NAME"]
        self.mongodb_result_collection = ConfigService.config["MONGODB_RESULT_COLLECTION"]
        self.mongodb_connection_timeout = ConfigService.config["MONGODB_CONNECTION_TIMEOUT_MS"]
        self.mongodb_socket_timeout = ConfigService.config["MONGODB_SOCKET_TIMEOUT_MS"]
        self.mongodb_server_selection_timeout = ConfigService.config["MONGODB_SERVER_SELECTION_TIMEOUT_MS"]

        self.emolex_word_col = ConfigService.config["EMOLEX_WORD_COL"]
        self.emolex_association_col = ConfigService.config["EMOLEX_ASSOCIATION_COL"]
        self.emolex_emotion_col = ConfigService.config["EMOLEX_EMOTION_COL"]
        self.emolex_delimiter = ConfigService.config["EMOLEX_DELIMITER"]

        self.number_emotions = ConfigService.config["NUMBER_OF_EMOTIONS"]
        self.batch_size = ConfigService.config["BATCH_SIZE"]
        self.send_batch_timeout = ConfigService.config["BATCH_SEND_TIMEOUT"]

        self.spark_local = ConfigService.config["SPARK_LOCAL"]

        self.spark_emolex_format = ConfigService.config["EMOLEX_FORMAT"]

        self.song_json_artist = ConfigService.config["SONG_JSON_ARTIST"]
        self.song_json_lyrics = ConfigService.config["SONG_JSON_LYRICS"]
        self.song_json_name = ConfigService.config["SONG_JSON_NAME"]

        self.base_path = ConfigService.config["BASE_PATH"]
        self.emotion_lex_path = ConfigService.config["NRC_EMOTION_LEX"]

        self.kafka_server_address = self.kafka_host + ":" + self.kafka_port
        self.mongodb_address = "mongodb://" + self.mongodb_host + ":" + self.mongodb_port + "/"
