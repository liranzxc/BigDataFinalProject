from pyspark import SparkConf
from pyspark import SparkContext

from services.config_service import ConfigService


class SparkService:
    def __init__(self):
        self.config = ConfigService()

    def get_spark_context(self):
        return SparkContext.getOrCreate(SparkConf().setMaster(self.config.spark_local))
