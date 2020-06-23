
def write_to_cassandra(df, table_name):

    def write_to_cassandra_impl(df, epochId):
        (
            df.write
                .option("checkpointLocation", '/tmp/check_point/')
                .format("org.apache.spark.sql.cassandra")
                .mode('append')
                .option("keyspace", "yelp_data")
                .option("table", table_name)
            .save()
        )

    (
        df.writeStream
            .outputMode("append")
            .foreachBatch(write_to_cassandra_impl)
            .start().awaitTermination()
     )