import datetime

from pyspark.sql import types as T
from pyspark.sql.functions import col, split, udf, from_json
from consumer.schemas.Checkin import CHECKIN_SCHEMA


def checkin_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), CHECKIN_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    df = raw_df.withColumn("date", split(col("date"), ","))

    def to_timestamp(list_of_timestamps):
        return [datetime.datetime.strptime(xx.strip(), '%Y-%m-%d %H:%M:%S') for xx in list_of_timestamps]

    to_timestamp_udf = udf(to_timestamp, T.ArrayType(T.TimestampType()))

    df = df.withColumn("date", to_timestamp_udf("date")).withColumnRenamed("date", "dates")
    return df
