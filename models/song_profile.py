class SongProfile:
    def __init__(self, number_of_words: int, histogram, emotion: str):
        # self.song = song
        self.number_of_words = number_of_words
        self.histogram = histogram
        self.emotion = emotion


    def upload_to_db(self):
        pass
