import pandas as pd
import json
from models.song import Song
from baseClasses.producer import Producer

json_songs = None
headers = None
artist_header_label = "artist"
song_name_header_label = "song_name"
lyrics_label = "text"
# jsons_songs = []
BOOTSTRAP_SERVER = "172.25.012:9092"
TOPIC_NAME = "read_csv_input_data"
producer = Producer(BOOTSTRAP_SERVER, TOPIC_NAME)


def read_csv(filepath = "datasets/songdata.csv"):
    global json_songs, headers, lyrics_json
    json_songs = pd.read_csv(filepath)
    json_songs.to_json(r'lyrics.json')
    headers = list(json_songs.columns)
    # print(headers)

    # print(lyrics_json)
    return headers, json_songs


def create_songs_list(lyrics_dataframe):
    songs_lst = []
    for row_index, row in lyrics_dataframe.iterrows():
        song_artist = row[artist_header_label]
        song_name = row[song_name_header_label]
        song_text = row[lyrics_label]
        songs_lst.append(Song(song_artist, song_name, song_text))

    return songs_lst


# def songs_list_to_jsons_list(songs_list):
#     jsons_songs = []
#     for song in songs_lst:
#         json.dump(song)


if __name__ == "__main__":
    read_csv()
    songs_lst = create_songs_list(json_songs)
    print(json_songs)

