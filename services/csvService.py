import pandas as pd
import json


class CsvService:
    @staticmethod
    def read_csv(filepath="datasets/songdata.csv"):
        df_songs = pd.read_csv(filepath)
        headers = list(df_songs.columns)
        songs_json = json.loads(df_songs.to_json(orient='records'))  ### save every row as json in file
        return df_songs, headers, songs_json
#
# def main():
#     df_songs, headers, songs_json = CsvService.read_csv()
#     producer = Producer(BOOTSTRAP_SERVER, TOPIC_NAME)
#     future = producer.send(songs_json[0])
#     result = future.get(timeout=0.5)
#     print(result)
#
#
# if __name__ == "__main__":
#     main()
