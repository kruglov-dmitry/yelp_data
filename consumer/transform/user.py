from pyspark.sql.functions import col, to_date, from_json, split
from consumer.schemas.Tip import TIP_SCHEMA


def user_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), TIP_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    """
    elite set<smallint>,
    
     set<varchar>,
    
    average_stars float
    """
    user_df = raw_df.withColumn(
        "elite",
        split(col("elite"), ",\s*").cast("array<int>").alias("elite")
    ).withColumn(
        "friends", split(col("friends"), ",\s*")
    )

    user_df = user_df.select("user_id", "name", to_date("yelping_since").alias("yelping_since"), "friends", "elite", "average_stars")

    user_statistic_df = raw_df.select("user_id", "review_count", "useful", "funny", "cool", "fans",
                                      "compliment_hot", "compliment_more", "compliment_profile",
                                      "compliment_cute", "compliment_list", "compliment_note",
                                      "compliment_plain", "compliment_cool", "compliment_funny",
                                      "compliment_writer", "compliment_photos")

    return user_statistic_df,
