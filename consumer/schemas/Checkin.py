from pyspark.sql import types as T

CHECKIN_SCHEMA = T.StructType(
    [
        T.StructField("business_id", T.StringType(), True),
        T.StructField("date", T.StringType(), True),
    ]
)
