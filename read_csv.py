import pandas as pd
import json



def read_csv(filepath = "datasets/songdata.csv"):
    lyrics_df = pd.read_csv(filepath)
    lyrics_df.to_json(r'lyrics.json')
    headers = list(lyrics_df.columns)
    print(headers)

    lyrics_json = lyrics_df.to_json(orient='split')
    # print(lyrics_json)
    return headers, lyrics_df, lyrics_json


# if __name__ == "__main__":
#     read_csv()

