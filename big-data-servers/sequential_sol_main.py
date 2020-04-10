from csv import reader
from services.config_service import ConfigService

artist_col_index = 0
song_name_col_index = 1
lyrics_col_index = 3



def count_words(str):
    counts = dict()
    words = str.split()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1

    return counts

if __name__ == "__main__":
    config = ConfigService()
    result_words_dict = dict()
    with open(config.song_lyrics_csv, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)
        # Iterate over each row in the csv using reader object
        iterrows = iter(csv_reader) # skip header
        next(iterrows)
        for row in iterrows:
            # row variable is a list that represents a row in csv
            song_name = row[song_name_col_index]
            artist_name = row[artist_col_index]
            count_dict = count_words(row[lyrics_col_index])
            if artist_name in result_words_dict:
                if song_name not in result_words_dict[artist_name]:
                    result_words_dict[artist_name][song_name] = count_dict
            else:
                result_words_dict[artist_name] = {}
                result_words_dict[artist_name][song_name] = count_dict
