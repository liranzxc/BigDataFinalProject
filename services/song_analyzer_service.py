# SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
from models.song import Song
from models.song_profile import SongProfile


class SongAnalyzerService:
    def __init__(self, sc):
        self.sc = sc

    # counts amount of words in the string
    def _count_words(self, rdd_lyrics_song):
        return rdd_lyrics_song.count()

    def _create_histogram(self, rdd_lyrics_song):
        return rdd_lyrics_song.map(lambda word: (word.lower(), 1)).reduceByKey(lambda a, b: a + b).collectAsMap()

    def _init_lyrics_rdd(self, song: Song):
        return self.sc.parallelize([song.lyrics]).flatMap(lambda line: line.split())\
            .map(lambda word : word.replace(".", ""))

    def analyze(self, song: Song):
        rdd_lyrics_song = self._init_lyrics_rdd(song)
        histogram = self._create_histogram(rdd_lyrics_song)
        word_count = self._count_words(rdd_lyrics_song)
        return SongProfile(song, word_count, histogram, None)  # emo none

