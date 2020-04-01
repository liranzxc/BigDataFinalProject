import pandas as pd
from nltk.stem import WordNetLemmatizer


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
