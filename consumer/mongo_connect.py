import pymongo


# based on this tutorial
# https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_installing.php


def get_mongo_db(hostname: str, port: int):
    myClient = pymongo.MongoClient("mongodb://" + hostname + ":" + str(port) + "/",
                                   connectTimeoutMS=5000, socketTimeoutMS=5000,serverSelectionTimeoutMS=2000)
    return myClient


if __name__ == "__main__":
    myClient = get_mongo_db('localhost', 27017)
    dbName = "test"
    mydb = myClient[dbName]
    dblist = myClient.list_database_names()
    print(dblist)
