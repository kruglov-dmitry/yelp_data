CREATE KEYSPACE IF NOT EXISTS yelp_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE yelp_data.review (
        review_id varchar,
        user_id varchar,
        business_id varchar,
        stars tinyint,
        review_date date,
        review_text varchar
    PRIMARY KEY (review_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details.
        review_id - string, 22 character unique string review id
        user_id - string, 22 character unique user id
        business_id - string, 22 character business id
        stars - star rating
        review_date - date of review
        review_text - the review itself
     '
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';

CREATE TABLE yelp_data.review_reactions (
        review_id varchar,
        useful counter,
        funny counter,
        cool counter
    PRIMARY KEY (review_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details.
        business_id - string, 22 character unique string business id
        dates - timestamps for each checkin'
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';