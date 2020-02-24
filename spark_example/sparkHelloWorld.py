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



####### Daniel HW1  ######

##### Q1 ####
import pyspark

conf = SparkConf().setAppName('lab2_q1').setMaster('local')
sc = SparkContext.getOrCreate(conf=conf)

file_path = 'randomWords'
#lines = sc.textFile(file_path)
output_path = "output"

#split words
words = sc.textFile(file_path).flatMap(lambda line: line.lower().split(" "))
# count the occurrence of each word
num_of_words = words.count()
print(f'Total number of words equals {num_of_words}')
word_counts = words.map(lambda word: (word, 1)).reduceByKey(lambda a,b:a+b)
word_counts = word_counts.sortBy(lambda a: a[1])
#count = word_counts.values().sum() #alternative way of counting
print(word_counts.collect())
word_counts.coalesce(1).saveAsTextFile(output_path)
sc.stop()


### Q2 ###
import pyspark

conf = SparkConf().setAppName('lab2_q2').setMaster('local')
sc = SparkContext.getOrCreate(conf=conf)

import random
def fill_points(K):
    result = []
    for i in range(K):
        a = random.uniform(-1, 1)
        b = random.uniform(-1, 1)
        result.append([a, b])
    return result

K = 10000
points = fill_points(K)
#print(points)

import math
rdd = sc.parallelize(points)
N = rdd.filter(lambda x: math.sqrt(x[0]**2 + x[1]**2) <= 1).count()
print(N)

pi = (4*N)/K
print(pi)
sc.stop