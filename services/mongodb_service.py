from models.song_profile import SongProfile
import pymongo
from utils.json_helpers import get_config_data

def get_mongo_db_client(hostname: str, port: str):
    myClient = pymongo.MongoClient("mongodb://" + hostname + ":" + port+ "/",
                                   connectTimeoutMS=5000, socketTimeoutMS=5000, serverSelectionTimeoutMS=2000)
    return myClient

class MongoDbService:
    def __init__(self):
        self.config = get_config_data()
        self.client = get_mongo_db_client(self.config["mongodb_ip"], self.config["mongodb_port"])
        self.db_name = self.config["mongodb_name"]
        # mydb = self.client[self.db_name]
        # db_list = self.client.list_database_names()
        # print(db_list)

    def upload_song_profiles(song_profiles: list[SongProfile]):
        pass