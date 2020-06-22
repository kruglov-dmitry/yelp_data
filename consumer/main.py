import argparse
import configparser

from pyspark.sql import SparkSession
from consumer.constants import KAFKA_TOPICS
from consumer.core.kafka import subscribe


def run_streaming_processing(spark, cfg, topic_id):
    transform_method = (arguments.tid)
    save_method = (cfg, arguments.tid)

    input_df = subscribe(spark, cfg, topic_id)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Streaming job startup script"
                                                 "--cfg file containing core settings"
                                                 "--tid name of kafka topic"
                                     )
    parser.add_argument('--cfg', action='store', required=True)
    parser.add_argument('--tid', choices=KAFKA_TOPICS, action='store', required=True)
    arguments = parser.parse_args()

    config = configparser.ConfigParser()
    config.read(arguments.cfg)

    spark = (
        SparkSession.builder.master(config["spark"]["master"])
            .appName(config["spark"]["app_name"])
            .config('spark.cassandra.connection.host', config["cassandra"]["host"])
            .config('spark.cassandra.connection.port', config["cassandra"]["port"])
            .config('spark.cassandra.output.consistency.level', config["cassandra"]["consistency"])
            .getOrCreate()
    )

    sc = spark.sparkContext

    sc.addPyFile("dependencies.zip")

    run_streaming_processing(spark, config, arguments.tid)
