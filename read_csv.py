import pandas as pd
import json
from baseClasses.consumer import Consumer
from baseClasses.producer import Producer

df_songs = None
lst_json_songs = []
headers = None
artist_header_label = "artist"
song_name_header_label = "song_name"
lyrics_label = "text"
BOOTSTRAP_SERVER = "172.25.012:9092"
TOPIC_NAME = "song"
producer = Producer(BOOTSTRAP_SERVER, TOPIC_NAME)


def read_csv(filepath = "datasets/songdata.csv"):
    global df_songs, headers, lst_json_songs
    df_songs = pd.read_csv(filepath)
    headers = list(df_songs.columns)
    df_songs.to_json(r'lyrics.json', orient='records', lines=True) ### save every row as json in file


# def get_json_songs():
#     global json_songs
#     with open('lyrics.json', 'r') as f:
#         data = f.read()
#         json_songs = json.loads(data)
#     pprint.pprint(json_songs)


def get_list_of_jsons():
    global lst_json_songs
    for line in open('lyrics.json', 'r'):
        lst_json_songs.append(json.loads(line))


if __name__ == "__main__":
    read_csv()
    get_list_of_jsons()
    consumer = Consumer(BOOTSTRAP_SERVER, TOPIC_NAME) #for test
   # print(lst_json_songs[0])
    future = (producer.send(lst_json_songs[0]))
    result = future.get(timeout=1)
    print(result)
    print("finish")

    # producer.producer.flush()
    # producer.producer.close()

    # for message in consumer:
    #     print(consumer)

