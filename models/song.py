class Song:
    def __init__(self, artist: str, name: str, lyrics: str):
        self.artist = artist
        self.name = name
        self.lyrics = lyrics

    @staticmethod
    def from_json_to_song(data):
        from services.config_service import ConfigService
        config = ConfigService()
        return Song(data[config.song_json_artist], data[config.song_json_name], data[config.song_json_lyrics])
