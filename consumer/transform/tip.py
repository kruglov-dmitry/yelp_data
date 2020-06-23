from pyspark.sql.functions import col, to_date, from_json, expr
from consumer.schemas.Tip import TIP_SCHEMA


def tip_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), TIP_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    df = raw_df.withColumn("tip_id", expr("uuid()"))

    tip_df = df.select("tip_id", "user_id", "business_id",
                       to_date("date").alias("tip_date"),
                       col("text").alias("tip_text"))

    tip_compliment_count_df = df.select("tip_id", "compliment_count")

    return tip_compliment_count_df, tip_df
