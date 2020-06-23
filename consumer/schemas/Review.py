from pyspark.sql import types as T

REVIEW_SCHEMA = T.StructType(
    [
        T.StructField("review_id", T.StringType(), True),
        T.StructField("user_id", T.StringType(), True),
        T.StructField("business_id", T.StringType(), True),
        T.StructField("stars", T.FloatType(), True),
        T.StructField("date", T.StringType(), True),
        T.StructField("text", T.StringType(), True),
        T.StructField("useful", T.IntegerType(), True),
        T.StructField("funny", T.IntegerType(), True),
        T.StructField("cool", T.IntegerType(), True),
    ]
)
