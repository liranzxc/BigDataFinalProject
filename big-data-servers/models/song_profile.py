from models.song import Song
import json


class SongProfile:
    def __init__(self, song: Song, number_of_words: int, histogram, emotion: list):
        self.song = song
        self.number_of_words = number_of_words
        self.histogram = histogram
        if emotion:
            self.emotion = emotion[0]
        else:
            self.emotion = ""

    def to_mongodb_document_format(self):
        return {"number_of_words": self.number_of_words, "histogram": self.histogram,
                "emotion": self.emotion, "song": json.dumps(self.song, default=lambda o: o.__dict__,
                                                            sort_keys=True, indent=4)}  # todo make more nice

    def __str__(self):
        t = "Analyzed song {0} by {1}\n".format(self.song.name, self.song.artist)
        t += "The song is {0} words long\n".format(self.number_of_words)
        t += "Lyrics histogram: {0}\n".format(self.histogram)
        t += "emotion: {0}".format(self.emotion)

        return t
