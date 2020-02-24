import pandas as pd
class NRC:
    def __init__(self, filePath="../datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
        self.emolex_df = pd.read_csv(filePath, names=["word", "emotion", "association"], skiprows=45, sep='\t')

    def findArrayOfFeelingByWord(self, word):
        return self.emolex_df[(self.emolex_df.word == word) & (self.emolex_df.association == 1)].emotion.values


## test
words = ["love", "happy", "kill"]
nrc = NRC()
for w in words:
    print(nrc.findArrayOfFeelingByWord(w))
    print(" " * 45)
