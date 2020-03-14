from pyspark import SparkConf
from pyspark import SparkContext


class SparkService:
    def __init__(self, config):
        self.config = config

    def get_spark_context(self):
        return SparkContext.getOrCreate(SparkConf().setMaster(self.config["SPARK_LOCAL"]))
