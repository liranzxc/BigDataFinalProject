from services.config_service import ConfigService
from nltk.stem import WordNetLemmatizer
import pandas as pd


class NRC:
    def __init__(self, config):
        self.config = config
        self.lemmatizer = WordNetLemmatizer()
        self.df = pd.read_csv(self.config.emotion_lex_path, names=["word", "emotion", "association"],
                              skiprows=45, sep='\t')

    def get_emotions_association(self, word):
        word = self.lemmatizer.lemmatize(word)
        selected_words = self.df[(self.df["word"] == word) & (self.df["association"] == 1)]
        return selected_words["emotion"].tolist()

#
# # test
# words = ["love", "happy", "kill"]
# nrc = NRC()
# nrc.get_emotions_association(words[0])