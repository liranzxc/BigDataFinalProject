# based on this tutorial
# https://www.bogotobogo.com/python/MongoDB_PyMongo/python_MongoDB_pyMongo_tutorial_installing.php


def get_mongo_db(hostname: str, port: int):
    address = hostname + ":" + str(port)
    from pymongo import MongoClient
    client = MongoClient(address)
    return client.myFirstMB


if __name__ == "__main__":
    db_example = get_mongo_db('localhost', 27017)
