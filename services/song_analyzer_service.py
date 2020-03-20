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

    def __get_emotion_histogram(self, word_histogram_map):
        emotions_string = r''
        for word in word_histogram_map:
            emotion_list = self.nrc.get_emotions_association(word)
            strength = word_histogram_map.get(word)
            for emotion in emotion_list:
                emotions_string += (emotion + " ") * strength

        emotion_histogram = self._create_histogram(self._get_words_rdd(emotions_string, clean=False))
        return emotion_histogram

    def analyze(self, song: Song, num_emotions=3):
        rdd_lyrics_song = self._get_words_rdd(song.lyrics)
        word_count = self._count_words(rdd_lyrics_song)
        histogram_words = self._create_histogram(rdd_lyrics_song)
        histogram_emotions = self.__get_emotion_histogram(word_histogram_map=histogram_words)
        ordered_emotions = sorted(histogram_emotions)
        emotion = ""
        for word in ordered_emotions[:num_emotions]:
            emotion += word + " "

        return SongProfile(song, word_count, histogram_words, emotion)  # emotion