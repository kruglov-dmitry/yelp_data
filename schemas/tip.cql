CREATE KEYSPACE IF NOT EXISTS yelp_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE yelp_data.tip (
        tip_id varchar,
        user_id varchar,
        business_id varchar,
        tip_date date,
        tip_text varchar
    PRIMARY KEY (tip_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details.
        tip_id - string, uuid unique identifier
        user_id - string, 22 character unique user id
        business_id - string, 22 character business id
        tip_date - date of review
        tip_text - the review itself
     '
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';

CREATE TABLE yelp_data.tip_compliment_count (
        tip_id varchar,
        compliment_count counter
    PRIMARY KEY (tip_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details.
        tip_id - string, uuid unique identifier
        compliment_count - integer, how many compliments it has
     '
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';