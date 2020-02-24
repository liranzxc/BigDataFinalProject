import pandas as pd

from pyspark import SparkConf
from pyspark import SparkContext
from pyspark.shell import sqlContext
from pyspark.sql import types
from pyspark.sql.functions import col


class NRC:
    def __init__(self, filePath="../datasets/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt"):
        self.sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
        print("connected to spark")
        df = sqlContext \
            .read.format("com.databricks.spark.csv") \
            .schema(self.schemaFile()).option("delimiter", "\t").load(filePath)
        cleanDF = df.na.drop()
        self.emolex_df = cleanDF

    def findArrayOfFeelingByWord(self, word):
        filterDF = self.emolex_df \
            .filter((col("word") == word) & (col("association") == 1)) \
            .select("emotion") \
            .collect()
        new_list = [row.emotion for row in filterDF]
        return new_list

    @staticmethod
    def schemaFile():
        schema = types.StructType(
            [
                types.StructField('word', types.StringType()),
                types.StructField('emotion', types.StringType()),
                types.StructField('association', types.IntegerType())
            ])
        return schema


## test
words = ["love", "happy", "kill"]
nrc = NRC()
for w in words:
    print(nrc.findArrayOfFeelingByWord(w))
    print(" " * 45)
