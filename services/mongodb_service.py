from models.song_profile import SongProfile
import pymongo
from config.configService import ConfigService
def get_mongo_db_client(hostname: str, port: str):
    myClient = pymongo.MongoClient("mongodb://" + hostname + ":" + port+ "/",
                                   connectTimeoutMS=5000, socketTimeoutMS=5000, serverSelectionTimeoutMS=2000)
    return myClient

class MongoDbService:
    def __init__(self):
        self.config = ConfigService.getConfig()
        self.client = get_mongo_db_client(self.config["MONGODB_HOST"], self.config["MONGODB_PORT"])
        self.db = self.config["MONGODB_NAME"]
        # mydb = self.client[self.db_name]
        # db_list = self.client.list_database_names()
        # print(db_list)

    def upload_song_profiles(self, song_profiles: list[SongProfile]):
        collection = self.db["MONGODB_RESULT_COLLECTION"]
        collection.insert_many(song_profiles)