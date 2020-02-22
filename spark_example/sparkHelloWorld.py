import os
import findspark
from pyspark import SparkConf
from pyspark import SparkContext

sc = SparkContext.getOrCreate(SparkConf().setMaster("local[*]"))
# will be connected to spark docker !


accum = sc.accumulator(0)

sc.parallelize([1, 2, 3, 4]).foreach(lambda x: accum.add(x))

print(accum.value)

# txt = sc.textFile('./text')
# print(txt.count())

# python_lines = txt.filter(lambda line: 'python' in line.lower())
# print(python_lines.count())
