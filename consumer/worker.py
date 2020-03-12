import re
from pyspark import SparkContext, SparkConf

from baseClasses.consumer import Consumer
from models.song import Song
import json

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))


# will be connected to spark docker !


def SongWork(song: Song):
    print("starting work on song ", song)
    print(song["artist"])
    print("here")


# counts amount of words in the string
def count_words(lyrics):
    delimiters = r'[.,\s]\t*\s*\n*'
    rdd = sc.parallelize([lyrics]).flatMap(lambda line: re.split(delimiters, line))
    return rdd.count()


if __name__ == "__main__":
    kafkaServer = "172.25.0.12:9092"
    topicReceive = "work"
    worker = Consumer(kafkaServer, topicReceive)

    worker.startReceive(SongWork)
    print("here")
    print(count_words("five one two three,     rff"))
