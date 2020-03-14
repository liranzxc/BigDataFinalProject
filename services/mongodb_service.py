from models.song_profile import SongProfile
import pymongo
from services.config_service import ConfigService


class MongoDbService:
    def __init__(self, config):
        self.config = config
        print(config)
        self.client = self._get_mongo_db_client(config["MONGODB_HOST"], config["MONGODB_PORT"])
        self.db_name = self.config["MONGODB_DB_NAME"]

    def _get_mongo_db_client(self, hostname: str, port: str):
        myClient = pymongo.MongoClient("mongodb://" + hostname + ":" + port + "/",
                                       connectTimeoutMS=5000, socketTimeoutMS=5000, serverSelectionTimeoutMS=2000)
        return myClient

    def upload_song_profiles(self, song_profiles: list):
        db = self.client[self.db_name]
        collection = db[self.config["MONGODB_RESULT_COLLECTION"]]
        return collection.insert_many(song_profiles)  ## status from db

    def get_all_records(self):
        db = self.client[self.db_name]
        collection = db[self.config["MONGODB_RESULT_COLLECTION"]]
        return collection.find()

