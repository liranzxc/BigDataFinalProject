from models.song import Song
from models.song_profile import SongProfile


def clean_word(word, allow_numbers=False):
    cleaned = ""
    numbers = '0123456789'
    not_allowed = '!,.?":;@#$%^&*()=+-\\'
    if not allow_numbers:
        not_allowed += numbers
    for char in word:
        if char in not_allowed:
            char = ""
        cleaned += char
    return cleaned


def clean_sentence(sentence):
    words1 = []
    words2 = sentence.split()
    for word in words2:
        word = clean_word(word)
        words1.append(word)
    return words1


class SongAnalyzerService:
    def __init__(self, sc, nrc):
        self.sc = sc
        self.nrc = nrc

    # counts amount of words in the string
    def _count_words(self, rdd_lyrics_song):
        return rdd_lyrics_song.count()

    def _create_histogram(self, rdd_lyrics):
        return rdd_lyrics.map(lambda word: word.lower()).countByValue()

    def _get_words_rdd(self, lyrics: str):
        rdd = self.sc.parallelize([lyrics]).flatMap(lambda line: clean_sentence(line))
        return rdd

    def _get_popular_emotion(self, histogram):
        emotion = []
        for w in sorted(histogram, key=histogram.get, reverse=True):
            emotion.extend(self.nrc.get_emotions_association(w))
            if len(emotion) is not 0:
                break
        return emotion

    def analyze(self, song: Song):
        rdd_lyrics_song = self._get_words_rdd(song.lyrics)
        word_count = self._count_words(rdd_lyrics_song)
        histogram_words = self._create_histogram(rdd_lyrics_song)
        emotion_list = self._get_popular_emotion(histogram=histogram_words)
        return SongProfile(song, word_count, histogram_words, emotion_list)  # emotion
