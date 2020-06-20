from pyspark.sql import types as T

TIP_SCHEMA = T.StructType(
    [
        T.StructField("text", T.StringType(), True),
        T.StructField("date", T.StringType(), True),
        T.StructField("compliment_count", T.IntegerType(), True),
        T.StructField("business_id", T.StringType(), True),
        T.StructField("user_id", T.StringType(), True),
    ]
)
