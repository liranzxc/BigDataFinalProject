import re
from string import ascii_lowercase as lower
from pyspark import SparkContext, SparkConf

from baseClasses.consumer import Consumer
from models.song import Song
import json

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))

# will be connected to spark docker !

delimiters = r'[.,\s]\t*\s*\n*'


def SongWork(song: Song):
    print("starting work on song ", song)
    print(song["artist"])
    print("here")


class SongAnalyzer:

    def __init__(self, song: Song):
        self.delimiters = r'[.,\s]\t*\s*\n*'
        self.song = song
        self.lyrics_rdd = self.init_lyrics_rdd()
        self.histogram = {}
        self.word_count = 0
        self.analyze()

    # counts amount of words in the string
    def count_words(self):
        return self.lyrics_rdd.count()

    def create_histogram(self):
        lyrics_map = self.lyrics_rdd.map(lambda word: (word.lower(), 1)).reduceByKey(lambda a, b: a + b).collectAsMap()
        return lyrics_map

    def init_lyrics_rdd(self):
        return sc.parallelize([self.song.lyrics]).flatMap(lambda line: re.split(delimiters, line))

    def analyze(self):
        self.histogram = self.create_histogram()
        self.word_count = self.count_words()

    def __str__(self):
        t = "Analyzed song {0} by {1}\n".format(self.song.name, self.song.artist)
        t += "The song is {0} words long\n".format(self.word_count)
        t += "Lyrics histogram: {0}".format(self.histogram)
        return t


if __name__ == "__main__":
    # kafkaServer = "172.25.0.12:9092"
    # topicReceive = "work"
    # worker = Consumer(kafkaServer, topicReceive)

    # worker.startReceive(SongWork)
    # print("here")

    lyrics = "Black is the night, metal we fight Power amps set to explode. Energy screams, magic and dreams Satan records the first note. We chime the bell, chaos and hell Metal for maniacs pure. Faster than steel, fortune on wheels Brain haemorrhage is the cure."
    analyzer = SongAnalyzer(Song("Venom", "Black Metal", lyrics))
    print(analyzer)
