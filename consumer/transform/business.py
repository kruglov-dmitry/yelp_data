from pyspark.sql import types as T
from pyspark.sql.functions import from_json, col, split, lit, create_map, udf
from itertools import chain
from consumer.schemas.Business import BUSINESS_SCHEMA, SCHEDULE_PER_DAY_SCHEMA


def business_transform(df):
    #
    #   Get payload from kafka msg
    #

    raw_df = df.select(
        from_json(col("value").cast("string"), BUSINESS_SCHEMA).alias("parsed_value")
    ).select("parsed_value.*")

    df = raw_df.withColumn("categories", split(col("categories"), ",\s*"))

    #
    #   struct_type to map
    #
    attributes_columns = df.select("attributes.*").columns
    attributes = create_map(list(chain(*((lit(name), col("attributes." + name)) for name in attributes_columns))))\
        .alias("attributes")

    df = df.select("business_id", "name", "address", "city", "state", "postal_code", "latitude",
                   "longitude", "stars", "is_open", attributes, "categories",
                   col("hours").cast(SCHEDULE_PER_DAY_SCHEMA))\
        .withColumn("is_open", (df.is_open == 1).cast(T.BooleanType()))

    #
    # remove nulls from maps
    #
    def filter_nulls(some_dict):
        if some_dict:
            return {k: some_dict[k] for k in some_dict if some_dict[k]}
        return {}

    filter_udf = udf(filter_nulls, T.MapType(T.StringType(), T.StringType()))

    #
    # result - two tables 1 to 1 mapping to C* schema
    #
    review_count_df = raw_df.select("business_id", "review_count")
    business_df = df.withColumn("attributes", filter_udf(df.attributes))

    return review_count_df, business_df
