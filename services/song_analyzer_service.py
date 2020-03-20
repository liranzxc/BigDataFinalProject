from utils.utilities import Utilities as ut
from models.song import Song
from models.song_profile import SongProfile


class SongAnalyzerService:
    def __init__(self, sc, nrc):
        self.sc = sc
        self.nrc = nrc

    # counts amount of words in the string
    def _count_words(self, rdd_lyrics_song):
        return rdd_lyrics_song.count()

    def _create_histogram(self, rdd_lyrics):
        return rdd_lyrics.map(lambda word: word.lower()).countByValue()

    #   Use clean=True if cleaning is needed
    #   Otherwise, the function assumes the lines are already clean, this is faster to compute
    def _get_words_rdd(self, lyrics: str, clean=True):
        if clean:
            rdd = self.sc.parallelize([lyrics]).flatMap(lambda line: ut.clean_sentence(line))
        else:
            rdd = self.sc.parallelize([lyrics]).flatMap(lambda line: line.split())
        return rdd

    def _get_emotion_histogram(self, word_histogram_map):
        most_word = max(word_histogram_map, key=lambda item: item[1])
        emotion_list = self.nrc.get_emotions_association(most_word[0])
        return emotion_list

    def analyze(self, song: Song, num_emotions=3):
        rdd_lyrics_song = self._get_words_rdd(song.lyrics)
        word_count = self._count_words(rdd_lyrics_song)
        histogram_words = self._create_histogram(rdd_lyrics_song)
        emotion_list = self._get_emotion_histogram(word_histogram_map=histogram_words)
        return SongProfile(song, word_count, histogram_words, emotion_list)  # emotion