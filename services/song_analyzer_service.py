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

    #   Use clean=True if cleaning is needed
    #   Otherwise, the function assumes the lines are already clean, this is faster to compute
    def _get_words(self, lyrics: str, clean=True):
        lyrics = lyrics.split("\n")
        words = []
        for line in lyrics:
            if clean:
                words.append(clean_sentence(line))
            else:
                words.append(line.split())
        return words

    def _get_emotion_histogram(self, word_histogram_map):
        emotion = []
        most_word = max(word_histogram_map.items(), key=lambda item: item[1])
        while
        emotion = self.nrc.get_emotions_association(most_word[0])
        return emotion

    def analyze(self, song: Song):
        word_database = self._get_words(song.lyrics)
        word_count = len(set(word_database))
        histogram_words = self._create_histogram(word_database)
        emotion = self._get_emotion_histogram(word_histogram_map=histogram_words)
        return SongProfile(song, word_count, histogram_words, emotion)  # emotion
