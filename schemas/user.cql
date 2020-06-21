CREATE KEYSPACE IF NOT EXISTS yelp_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;

CREATE TABLE yelp_data.user_statistics (
    user_id varchar,
    review_count counter,
    useful counter,
    funny counter,
    cool counter,
    fans counter,
    compliment_hot counter,
    compliment_more counter,
    compliment_profile counter,
    compliment_cute counter,
    compliment_list counter,
    compliment_note counter,
    compliment_plain counter,
    compliment_cool counter,
    compliment_funny counter,
    compliment_writer counter,
    compliment_photos counter
PRIMARY KEY (user_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds user details.
        user_id - string, 22 character unique user id
        review_count - integer, the number of reviews they've written
        useful - number of useful votes sent by the user
        funny - number of funny votes sent by the user
        cool - number of cool votes sent by the user
        fans - number of fans the user has
        compliment_hot - number of hot compliments received by the user
        compliment_more - number of more compliments received by the user
        compliment_profile - number of profile compliments received by the user
        compliment_cute - number of cute compliments received by the user
        compliment_list - number of list compliments received by the user
        compliment_note - number of note compliments received by the user
        compliment_plain - number of plain compliments received by the user
        compliment_cool - number of cool compliments received by the user
        compliment_funny - number of funny compliments received by the user
        compliment_writer - number of writer compliments received by the user
        compliment_photos - number of photo compliments received by the user
    '
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';


CREATE TABLE yelp_data.user (
    user_id varchar,
    name varchar,
    yelping_since date,
    friends set<varchar>,
    elite set<smallint>,
    average_stars float
    PRIMARY KEY (user_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds user details.
        user_id - string, 22 character unique user id
        name - string, the user's first name
        yelping_since - when the user joined Yelp
        friends - array of the user's friends as user_ids
        elite - the years the user was elite
        average_stars - float, average rating of all reviews
    '
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.SizeTieredCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';