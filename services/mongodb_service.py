from models.song_profile import SongProfile
import pymongo
from services.config_service import ConfigService



class MongoDbService:
    def __init__(self):
        self.config = ConfigService.getConfig()
        self.client = self.get_mongo_db_client(self.config["MONGODB_HOST"], self.config["MONGODB_PORT"])
        self.db = self.config["MONGODB_DB_NAME"]

    def get_mongo_db_client(self, hostname: str, port: str):
        myClient = pymongo.MongoClient("mongodb://" + hostname + ":" + port + "/",
                                       connectTimeoutMS=5000, socketTimeoutMS=5000, serverSelectionTimeoutMS=2000)
        return myClient

    def upload_song_profiles(self, song_profiles : list):
        collection = self.db["MONGODB_RESULT_COLLECTION"]
        collection.insert_many(song_profiles)