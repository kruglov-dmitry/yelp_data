

def subscribe(spark, cfg, topic_name):

    #
    #   FIXME NOTE: yep, we can externalize and inject other config here as well
    #

    return spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", cfg.get("kafka", "broker")) \
        .option("subscribe", topic_name) \
        .option("maxOffsetsPerTrigger", 5) \
        .option("startingOffsets", "earliest") \
        .load()
