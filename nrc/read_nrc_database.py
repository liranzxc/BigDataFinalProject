from services.config_service import ConfigService
from pyspark.shell import sqlContext
from pyspark.sql import types
from pyspark.sql.functions import col
from nltk.stem import WordNetLemmatizer


class NRC:
    def __init__(self, file_path="datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
        config_service = ConfigService()
        self.config = config_service.getConfig()
        print("nrc connected to spark")
        df = sqlContext \
            .read.format("com.databricks.spark.csv") \
            .schema(self.schema_file()).option("delimiter", "\t").load(file_path)
        clean_df = df.na.drop()
        self.emotion_lex_df = clean_df
        self.lemmatizer = WordNetLemmatizer()

    def get_emotions_association(self, word):
        word = self.lemmatizer.lemmatize(word)
        filter_df = self.emotion_lex_df \
            .filter((col("word") == word) & (col("association") == 1)) \
            .select("emotion") \
            .collect()
        new_list = [row.emotion for row in filter_df]
        return new_list

    @staticmethod
    def schema_file():
        schema = types.StructType(
            [
                types.StructField('word', types.StringType()),
                types.StructField('emotion', types.StringType()),
                types.StructField('association', types.IntegerType())
            ])
        return schema

## test
# words = ["love", "happy", "kill"]
# nrc = NRC()
# for w in words:
#    print(nrc.findArrayOfFeelingByWord(w))
#    print(" " * 45)
