import json

import pandas as pd


class CsvService:
    @staticmethod
    def read_csv(filepath="datasets/songdata.csv"):
        df_songs = pd.read_csv(filepath)
        headers = list(df_songs.columns)
        songs_json = json.loads(df_songs.to_json(orient='records'))  ### save every row as json in file
        return df_songs, headers, songs_json
