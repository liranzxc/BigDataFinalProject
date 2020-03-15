# SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
from pyspark import SparkContext, SparkConf
from utils.utilities import Utilities as ut
from models.song import Song
from models.song_profile import SongProfile


class SongAnalyzerService:
    def __init__(self, sc):
        self.sc = sc

    # counts amount of words in the string
    def _count_words(self, rdd_lyrics_song):
        return rdd_lyrics_song.count()

    def _create_histogram(self, rdd_lyrics):
        return rdd_lyrics.map(lambda word: (word.lower(), 1)).reduceByKey(lambda a, b: a + b)

    def _create_histogram_as_map(self, histogram_rdd):
        return histogram_rdd.collectAsMap()

    def _init_lyrics_rdd(self, song: Song):
        return self.sc.parallelize([song.lyrics]).flatMap(lambda line: ut.clean_sentence(line))

    def __get_emotion(self, histogram_rdd):
        emotion = 'happy'
        return emotion

    def analyze(self, song: Song):
        rdd_lyrics_song = self._init_lyrics_rdd(song)
        word_count = self._count_words(rdd_lyrics_song)

        histogram_rdd = self._create_histogram(rdd_lyrics_song)
        histogram_map = self._create_histogram_as_map(histogram_rdd)

        emotion = self.__get_emotion(histogram_rdd=histogram_rdd)
        return SongProfile(song, word_count, histogram_map, emotion)  # emotion


if __name__ == "__main__":
    sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
    lyrics = "Black is the night..., metal@# we fight Power amps set to explode. Energy screams, magic and dreams Satan records the first note. We chime the bell, chaos and hell Metal for maniacs pure. Faster than steel, fortune on wheels Brain haemorrhage is the cure."
    song1 = Song("Venom", "Black Metal", lyrics)
    analyzer = SongAnalyzerService(sc)
    print(analyzer.analyze(song1))
    #lyrics = ut.clean_sentence(lyrics)
    #print(lyrics)
