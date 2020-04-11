from csv import reader
from services.config_service import ConfigService
import time
from services.nrc_service import NRC


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

def get_emotion(words_counts_tuples, nrc):
    emotion = []
    for tuple in words_counts_tuples:
        word = tuple[0]
        emotion.extend(nrc.get_emotions_association(word))
        if len(emotion) is not 0:
            break
    return emotion

if __name__ == "__main__":
    config = ConfigService()
    result_words_dict = dict()
    t = time.process_time()
    emotions = {}

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
            sorted_count_dict = sorted(count_dict.items(), key=lambda x: x[1], reverse=True)
            song_emotions = get_emotion(sorted_count_dict, NRC(config))
            if artist_name in result_words_dict:
                result_words_dict[artist_name][song_name] = sorted_count_dict
            else:
                result_words_dict[artist_name] = {}
                emotions[artist_name] = {}
                result_words_dict[artist_name][song_name] = sorted_count_dict
            emotions[artist_name][song_name] = song_emotions
            print("iteration ended")

    elapsed_time = time.process_time() - t
    print(f'Time elapsed since word count started: {elapsed_time}')
