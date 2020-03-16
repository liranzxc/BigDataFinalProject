from services.config_service import ConfigService
from pyspark.shell import sqlContext
from pyspark.sql import types
from pyspark.sql.functions import col
from nltk.stem import WordNetLemmatizer


class NRC:

    def __init__(self):
        self.config = ConfigService()
        print("nrc connected to spark")
        df = sqlContext \
            .read.format(self.config.spark_emolex_format) \
            .schema(self.schema_file()).option("delimiter", self.config.emolex_delimiter).load(self.config.emotion_lex_path)
        clean_df = df.na.drop()
        self.emotion_lex_df = clean_df
        self.lemmatizer = WordNetLemmatizer()

    def get_emotions_association(self, word):
        word = self.lemmatizer.lemmatize(word)
        filter_df = self.emotion_lex_df \
            .filter((col(self.config.emolex_word_col) == word) & (col(self.config.emolex_association_col) == 1)) \
            .select(self.config.emolex_emotion_col) \
            .collect()
        new_list = [row.emotion for row in filter_df]
        return new_list

    @staticmethod
    def schema_file():
        config = ConfigService()
        schema = types.StructType(
            [
                types.StructField(config.emolex_word_col, types.StringType()),
                types.StructField(config.emolex_emotion_col, types.StringType()),
                types.StructField(config.emolex_association_col, types.IntegerType())
            ])
        return schema

## test
# words = ["love", "happy", "kill"]
# nrc = NRC()
# for w in words:
#    print(nrc.findArrayOfFeelingByWord(w))
#    print(" " * 45)
