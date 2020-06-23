from array import array
from pyspark.sql import types as T
from pyspark.sql.functions import col, to_date, from_json, split, udf
from consumer.schemas.Tip import TIP_SCHEMA


def user_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), TIP_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    user_df = raw_df.withColumn(
        "elite",
        split(col("elite"), ",\s*").alias("elite")
    ).withColumn(
        "friends", split(col("friends"), ",\s*")
    )

    #
    # remove nulls from maps
    #
    #   NOTE: https://adatis.co.uk/databricks-udf-performance-comparisons/
    #
    def filter_nulls(some_set):
        w = array("h")
        if some_set:
            for x in some_set:
                try:
                    w.append(int(x))
                except:
                    pass
        return w

    filter_udf = udf(filter_nulls, T.ArrayType(T.ShortType()))
    user_df = user_df.withColumn("elite", filter_udf(user_df.elite))

    user_df = user_df.select("user_id", "name", to_date("yelping_since").alias("yelping_since"),
                             "friends", "elite", "average_stars")

    user_statistic_df = raw_df.select("user_id", "review_count", "useful", "funny", "cool", "fans",
                                      "compliment_hot", "compliment_more", "compliment_profile",
                                      "compliment_cute", "compliment_list", "compliment_note",
                                      "compliment_plain", "compliment_cool", "compliment_funny",
                                      "compliment_writer", "compliment_photos")

    return user_statistic_df, user_df
