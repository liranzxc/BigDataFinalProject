import re

import pymongo


class MongoDbService:
    def __init__(self, config):
        self.config = config
        self.client = self._get_mongo_db_client()
        self.db_name = self.config.mongodb_db_name
        self.db_result = self.config.mongodb_result_collection

    def _get_mongo_db_client(self):
        my_client = pymongo.MongoClient(self.config.mongodb_address,
                                        connectTimeoutMS=self.config.mongodb_connection_timeout,
                                        socketTimeoutMS=self.config.mongodb_socket_timeout,
                                        serverSelectionTimeoutMS=self.config.mongodb_server_selection_timeout)
        return my_client

    def upload_song_profiles(self, song_profiles: list):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        return collection.insert_many(song_profiles)  ## status from db

    def upload_song_profile(self, song_profile: dict):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        return collection.insert(song_profile)  ## status from db

    def get_all_records(self, page=-1, size=-1):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        if page > -1 and size > -1:
            return collection.find().skip(page * size).limit(size)
        else:
            return collection.find()

    def get_records_artist_by_letter(self, page=-1, size=-1, letter='A'):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        regx = re.compile("^" + letter, re.IGNORECASE)
        if page > -1 and size > -1:
            return collection.find({"artist": regx}).skip(page * size).limit(size)
        else:
            return collection.find({"artist": regx})

    def get_counts(self):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        return collection.find().count()

    def delete_all_records(self):
        db = self.client[self.db_name]
        collection = db[self.db_result]
        return collection.delete_many({})
