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
    def __init__(self, nrc):
        self.nrc = nrc

    def _create_histogram(self, word_database):
        word_histogram = {}
        word_set = set(word_database)
        for word in word_set:
            word_histogram[word] = word_database.count(word)
        return word_histogram

    def _get_words(self, lyrics: str):
        lyrics = lyrics.split("\r\n")
        words = []
        for line in lyrics:
            words.append(clean_sentence(line))
        return words

    def _get_emotion_histogram(self, map):
        emotion = []
        for w in sorted(map, key=map.get, reverse=True):
            emotion.append(self.nrc.get_emotions_association(w))
            if len(emotion):
                break
        return emotion

    def analyze(self, song: Song):
        word_database = self._get_words(song.lyrics)
        word_count = len(set(word_database))
        histogram_words = self._create_histogram(word_database)
        emotion = self._get_emotion_histogram(map=histogram_words)
        return SongProfile(song, word_count, histogram_words, emotion)
