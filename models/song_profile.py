from models.song import Song


class SongProfile:
    def __init__(self, song: Song, number_of_words: int, histogram, emotion: str):
        self.song = song
        self.number_of_words = number_of_words
        self.histogram = histogram
        self.emotion = emotion

    def to_mongodb_document_format(self):
        song_profile_id = self.song.artist + "_" + self.song.name
        return {"_id": song_profile_id, "number_of_words": self.number_of_words, "histogram": self.histogram, "emotion": self.emotion}