from pyspark.sql import types as T

USER_SCHEMA = T.StructType(
    [
        T.StructField("user_id", T.StringType(), True),
        T.StructField("name", T.StringType(), True),
        T.StructField("review_count", T.IntegerType(), True),
        T.StructField("yelping_since", T.StringType(), True),
        T.StructField("friends", T.StringType(), True),
        T.StructField("useful", T.IntegerType(), True),
        T.StructField("funny", T.IntegerType(), True),
        T.StructField("cool", T.IntegerType(), True),
        T.StructField("fans", T.IntegerType(), True),
        T.StructField("elite", T.StringType(), True),
        T.StructField("average_stars", T.FloatType(), True),
        T.StructField("compliment_hot", T.IntegerType(), True),
        T.StructField("compliment_more", T.IntegerType(), True),
        T.StructField("compliment_profile", T.IntegerType(), True),
        T.StructField("compliment_cute", T.IntegerType(), True),
        T.StructField("compliment_list", T.IntegerType(), True),
        T.StructField("compliment_note", T.IntegerType(), True),
        T.StructField("compliment_plain", T.IntegerType(), True),
        T.StructField("compliment_cool", T.IntegerType(), True),
        T.StructField("compliment_funny", T.IntegerType(), True),
        T.StructField("compliment_writer", T.IntegerType(), True),
        T.StructField("compliment_photos", T.IntegerType(), True),
    ]
)
