import pandas as pd
import json
from models.song import Song

lyrics_df = None
headers = None
artist_header_label = "artist"
song_name_header_label = "song_name"
lyrics_label = "text"
lyrics_json = None

def read_csv(filepath = "datasets/songdata.csv"):
    global lyrics_df, headers, lyrics_json
    lyrics_df = pd.read_csv(filepath)
    lyrics_df.to_json(r'lyrics.json')
    headers = list(lyrics_df.columns)
    # print(headers)

    lyrics_json = lyrics_df.to_json(orient='split')
    # print(lyrics_json)
    return headers, lyrics_df, lyrics_json

def create_songs_list(lyrics_dataframe):
    songs_lst = []
    for row_index, row in lyrics_dataframe.iterrows():
        song_artist = row[artist_header_label]
        song_name = row[song_name_header_label]
        song_text = row[lyrics_label]
        songs_lst.append(Song(song_artist, song_name, song_text))

    return songs_lst

if __name__ == "__main__":
    read_csv()
    create_songs_list(lyrics_df)

