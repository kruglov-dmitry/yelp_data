def write_to_cassandra(df, epochId):
    (
        df.write
            .option("checkpointLocation", '/tmp/check_point/')
            .format("org.apache.spark.sql.cassandra")
            .mode('append')
            .option("keyspace", "yelp_data")
            .option("table", "business_review_count")
        .save()
    )
