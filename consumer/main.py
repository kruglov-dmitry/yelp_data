import sys

# from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils

import pyspark.sql.functions as f

from schemas.Business import BUSINESS_SCHEMA

def some_method(x):
	return f.from_json(x[1], BUSINESS_SCHEMA)	

if __name__ == "__main__":
    spark = SparkSession.builder.master("local").getOrCreate()
    sc = spark.sparkContext
    sc.addPyFile("dependencies.zip")

    ssc = StreamingContext(sc, 2)
    kvs = KafkaUtils.createDirectStream(ssc, ["business"], {"metadata.broker.list": "192.168.0.9:9092", "auto.offset.reset": "smallest"})
    b = kvs.map(some_method)
    
    b.pprint(5)
    ssc.start()
    ssc.awaitTermination()
