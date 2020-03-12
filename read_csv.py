import pandas as pd
import json
from baseClasses.consumer import Consumer
from baseClasses.producer import Producer

# artist_header_label = "artist"
# song_name_header_label = "song_name"
# lyrics_label = "text"
BOOTSTRAP_SERVER = "172.25.0.12:9092"
TOPIC_NAME = "song"


def read_csv(filepath="datasets/songdata.csv"):
    df_songs = pd.read_csv(filepath)
    headers = list(df_songs.columns)
    songs_json = json.loads(df_songs.to_json(orient='records'))  ### save every row as json in file
    return df_songs, headers, songs_json


# def get_json_songs():
#     global json_songs
#     with open('lyrics.json', 'r') as f:
#         data = f.read()
#         json_songs = json.loads(data)
#     pprint.pprint(json_songs)


if __name__ == "__main__":
    df_songs, headers, songs_json = read_csv()
    producer = Producer(BOOTSTRAP_SERVER, TOPIC_NAME)
    future = producer.send(songs_json[0])
    result = future.get(timeout=0.5)
