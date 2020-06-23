CREATE KEYSPACE IF NOT EXISTS yelp_data WITH replication = {'class': 'SimpleStrategy', 'replication_factor': '1'}  AND durable_writes = true;
 
 CREATE TYPE yelp_data.schedule_per_day (
   monday varchar,
   tuesday varchar,
   wednesday varchar,
   thursday varchar,
   friday varchar,
   saturday varchar,
   sunday varchar
 );

CREATE TABLE yelp_data.business (
    business_id varchar,
    name varchar,
    address varchar,
    city varchar,
    state varchar,
    postal_code varchar,
    latitude float,
    longitude float,
    stars float,
    is_open boolean,
    attributes map<varchar, varchar>,
    categories set<varchar>,
    hours FROZEN<schedule_per_day>,
    PRIMARY KEY (business_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details.
        business_id - string, 22 character unique string business id
        name - string, the business s name,
        address - string, the full address of the business,
        city - string, the city,
        state - string, 2 character state code, if applicable,
        postal_code - string, the postal code,
        latitude - float, latitude,
        longitude - float, longitude,
        stars - float, star rating, rounded to half-stars,
        is_open - boolean,
        attributes - map of string => string i.e. attribute name attribute value,
        note: some attribute values might be objects,
        categories - set of strings of business categories,
        hours - an object of key day to value hours, hours are using a 24hr clock'
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';

CREATE TABLE yelp_data.business_review_count (
    business_id varchar,
    review_count counter,
    PRIMARY KEY (business_id)
) WITH bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds count of reviews for business.
        business_id - string, 22 character unique string business id
        review_count - integer, number of reviews'
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';


CREATE TABLE yelp_data.business_by_location (
    geo_hash varchar,
    category varchar,
    business_id varchar,
    name varchar,
    address varchar,
    city varchar,
    state varchar,
    postal_code varchar,
    latitude float,
    longitude float,
    stars float,
    is_open boolean,
    attributes map<varchar, varchar>,
    hours FROZEN<schedule_per_day>,
    PRIMARY KEY (geo_hash, category, stars, business_id)
) WITH CLUSTERING ORDER BY (category DESC, stars DESC, business_id DESC)
    AND bloom_filter_fp_chance = 0.01
    AND caching = {'keys':'ALL', 'rows_per_partition':'NONE'}
    AND comment = 'Table holds business details ordered by location, category, rating.
        geo_hash - geo hash string computed based lat and long
        category - one of category specific to business
        business_id - string, 22 character unique string business id
        name - string, the business s name,
        address - string, the full address of the business,
        city - string, the city,
        state - string, 2 character state code, if applicable,
        postal_code - string, the postal code,
        latitude - float, latitude,
        longitude - float, longitude,
        stars - float, star rating, rounded to half-stars,
        is_open - boolean,
        attributes - map of string => string i.e. attribute name attribute value,
        note: some attribute values might be objects,
        hours - an object of key day to value hours, hours are using a 24hr clock'
    AND compaction = {'class': 'org.apache.cassandra.db.compaction.LeveledCompactionStrategy'}
    AND compression = {'sstable_compression': 'org.apache.cassandra.io.compress.DeflateCompressor'}
    AND default_time_to_live = 0
    AND gc_grace_seconds = 864000
    AND max_index_interval = 2048
    AND memtable_flush_period_in_ms = 0
    AND min_index_interval = 128
    AND speculative_retry = '99.0PERCENTILE';
