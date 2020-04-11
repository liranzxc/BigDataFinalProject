from csv import reader

from models.song import Song
from models.song_profile import SongProfile
from services.config_service import ConfigService
import time
from services.nrc_service import NRC

ARTIST_COL = 0
SONG_NAME_COL = 1
LYRICS_COL = 3


def word_histogram(words):
    counts = dict()

    for word in words:
        if word in counts:
            counts[word] += 1
        else:
            counts[word] = 1
    return counts


def get_emotion(words_counts_tuples, _nrc):
    emotion = []
    for _tuple in words_counts_tuples:
        word = _tuple[0]
        emotion.extend(_nrc.get_emotions_association(word))
        if len(emotion) is not 0:
            break
    return emotion


def clean_word(word, allow_numbers=False):
    cleaned = ""
    numbers = '0123456789'
    not_allowed = '!,.?":;@#$%^&*[]{}()=+-\\'
    if not allow_numbers:
        not_allowed += numbers
    for char in word:
        if char in not_allowed:
            char = ""
        cleaned += char
    return cleaned


def clean_sentence(sentence):
    words1 = []
    words2 = sentence.split()
    for word in words2:
        word = clean_word(word).lower()
        words1.append(word)
    return words1


def clean_lyrics(lyrics_str):
    lyrics_lst = []
    lyrics_str = lyrics_str.split("\r\n")
    for line in lyrics_str:
        lyrics_lst.extend(clean_sentence(line))
    return lyrics_lst


if __name__ == "__main__":
    config = ConfigService()
    result_words_dict = dict()
    t = time.process_time()
    profiles = []
    nrc = NRC(config)
    with open(config.song_lyrics_csv, 'r') as read_obj:
        # pass the file object to reader() to get the reader object
        csv_reader = reader(read_obj)

        # Iterate over each row in the csv using reader object
        iterrows = iter(csv_reader)
        next(iterrows)  # skip header

        for index, row in enumerate(iterrows):
            # row represents a song entry in csv
            song_name = row[SONG_NAME_COL]
            artist_name = row[ARTIST_COL]
            lyrics = row[LYRICS_COL]
            song = Song(artist=artist_name, name=song_name, lyrics=lyrics)
            lyrics = clean_lyrics(lyrics)
            count = len(lyrics)
            histogram = word_histogram(lyrics)
            sorted_histogram = sorted(histogram.items(), key=lambda x: x[1], reverse=True)
            song_emotions = get_emotion(sorted_histogram, nrc)
            profile = SongProfile(song=song, number_of_words=count, histogram=histogram, emotion=song_emotions)
            profiles.append(profile)
            print("song {0} analyzed".format(index))
            print(profile)

    elapsed_time = time.process_time() - t
    print(f'Time elapsed since song analysis started: {elapsed_time}')
