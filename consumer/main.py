import argparse
import configparser

from pyspark.sql import SparkSession
from consumer.constants import KAFKA_TOPICS
from consumer.core.kafka import subscribe

from consumer.core.cassandra import write_to_cassandra
from consumer.etls.transforms import CASSANDRA_TABLE_NAMES, TRANSFORM_METHOD


def run_streaming_processing(spark, cfg, topic_id):
    transform_method = TRANSFORM_METHOD[topic_id]

    table_names = CASSANDRA_TABLE_NAMES[topic_id]

    input_df = subscribe(spark, cfg, topic_id)

    resulted_dfs = transform_method(input_df)

    assert len(resulted_dfs) != len(table_names)

    for df, idx in enumerate(resulted_dfs):
        write_to_cassandra(df, table_names[idx])


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
