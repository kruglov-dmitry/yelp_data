from threading import Thread
import time

import argparse
import configparser as cfgr

from pyspark.sql import SparkSession
from consumer.constants import KAFKA_TOPICS
from consumer.core.kafka import subscribe

from consumer.core.cassandra import write_to_cassandra
from consumer.transform.transforms import CASSANDRA_TABLE_NAMES, TRANSFORM_METHOD

def start_process_daemon(method, args):
    new_thread = Thread(target=method, args=args)
    new_thread.daemon = True
    new_thread.start()

def run_streaming_processing(spark, cfg, topic_id):
    transform_method = TRANSFORM_METHOD[topic_id]

    table_names = CASSANDRA_TABLE_NAMES[topic_id]

    input_df = subscribe(spark, cfg, topic_id)

    resulted_dfs = transform_method(input_df)

    assert len(resulted_dfs) == len(table_names)

    for idx, df in enumerate(resulted_dfs):
        start_process_daemon(write_to_cassandra, (df, table_names[idx]))

    #
    #   To handle CTRL-C properly
    #
    while True:
        time.sleep(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Streaming job startup script"
                                                 "--cfg file containing core settings"
                                                 "--tid name of kafka topic"
                                     )
    parser.add_argument('--cfg', action='store', required=True)
    parser.add_argument('--tid', choices=KAFKA_TOPICS, action='store', required=True)
    arguments = parser.parse_args()

    config = cfgr.ConfigParser(interpolation=cfgr.ExtendedInterpolation())
    config.read(arguments.cfg)

    DEPENDENCIES = 'org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0,com.datastax.spark:spark-cassandra-connector_2.11:2.4.0'

    spark = (
        SparkSession.builder.master(config["spark"]["master"])
            .appName(config["spark"]["app_name"])
            .config('spark.jars.packages', DEPENDENCIES)
            .config('spark.cassandra.connection.host', config["cassandra"]["host"])
            .config('spark.cassandra.connection.port', config["cassandra"]["port"])
            .config('spark.cassandra.output.consistency.level', config["cassandra"]["consistency"])
            .getOrCreate()
    )

    sc = spark.sparkContext

    #
    # sc.addPyFile("dependencies.zip")
    #

    run_streaming_processing(spark, config, arguments.tid)
