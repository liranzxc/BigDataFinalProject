class Song:
    def __init__(self, artist: str, name: str, lyrics: str):
        self.artist = artist
        self.name = name
        self.lyrics = lyrics

    @staticmethod
    def from_json_to_song(data):
        return Song(data["artist"], data["song_name"], data["text"])
