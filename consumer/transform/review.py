from pyspark.sql import types as T
from pyspark.sql.functions import col, to_date, from_json
from consumer.schemas.Review import REVIEW_SCHEMA


def review_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), REVIEW_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    review_df = raw_df.select("review_id", "user_id", "business_id",
                              col("stars").cast(T.ByteType()),
                              to_date("date").alias("review_date"),
                              col("text").alias("review_text")
                              )

    #
    # result - two tables 1 to 1 mapping to C* schema
    #
    review_reactions_df = raw_df.select("review_id", "useful", "funny", "cool")

    return review_reactions_df, review_df
