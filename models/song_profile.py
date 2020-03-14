from models.song import Song
import uuid


class SongProfile:
    def __init__(self, song: Song, number_of_words: int, histogram, emotion: str):
        self.song = song
        self.number_of_words = number_of_words
        self.histogram = histogram
        self.emotion = emotion

    def to_mongodb_document_format(self):
        return {"number_of_words": self.number_of_words, "histogram": self.histogram,
                "emotion": self.emotion}  # todo add song to json

    def __str__(self):
        t = "Analyzed song {0} by {1}\n".format(self.song.name, self.song.artist)
        t += "The song is {0} words long\n".format(self.number_of_words)
        t += "Lyrics histogram: {0}\n".format(self.histogram)
        t += "emotion: {0}".format(self.emotion)

        return t
