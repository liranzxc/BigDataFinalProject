
#SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
class SongAnalyzerService:
    def __init__(self,sc):
        self.sc = sc

    # counts amount of words in the string
    def _count_words(self,rdd_lyrics_song):
        return rdd_lyrics_song.count()

    def _create_histogram(self,rdd_lyrics_song):
        return rdd_lyrics_song.map(lambda word: (word.lower(), 1)).reduceByKey(lambda a, b: a + b).collectAsMap()

    def _init_lyrics_rdd(self,song:Song):
        return self.sc.parallelize([song.lyrics]).flatMap(lambda line: line.split())

    def analyze(self,song:Song) :
        rdd_lyrics_song = self._init_lyrics_rdd(song)
        histogram = self._create_histogram(rdd_lyrics_song)
        word_count = self._count_words(rdd_lyrics_song)
        return  SongProfile(song,word_count,histogram,None)# emo none


    #
    # def __str__(self):
    #     t = "Analyzed song {0} by {1}\n".format(self.song.name, self.song.artist)
    #     t += "The song is {0} words long\n".format(self.word_count)
    #     t += "Lyrics histogram: {0}".format(self.histogram)
    #     return t
