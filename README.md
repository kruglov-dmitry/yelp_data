# TODO
setup:
- schema in cassandra
Spark streaming job => Kafka => Cassandra
Data Quality Assurance - aka e2e tests?
ETL(?) logic autotests?

# Simplification
- kafka topics replication & partitions
- cassandra replication factor
- number of nodes in setup decreased to have options to be able 
to run all setup within single laptop

## Data schema modeling:
General consideration - Cassandra schema usually defined based on requirements of how user will query data.

I made assumptions that we may need to answer efficiently these kind of questions:
-

Data modifications in comparison to raw data:

data are imported as is into base tables:
- yelp_data.business
- yelp_data.review + yelp_data.review_reactions
- yelp_data.checkin

For future it depend on use case i.e. if we need to retrieve businesses by locations, category and rating for examples
we will infer data from base table - yelp_data.business 
and created dedicated table with appropriate indexes - i.e. PK will be geohash(lat, long): String, category, rating

add last_review first?
  

Business:
- postal code - initial intention was to cast it to integer, but look up at Wiki reveal that for some countries it may contains letters
- is_open - from integer to boolean
- attributes to map (only programmatic filtering)
- hours - to udt (only programmatic filtering)

Counters for business, should be updated independent from main records
- reviews
- stars

Checkin:
- date (String) -> set<timestamp>

Reverse indexes:
category -> business_ids + hours + location (lat, long)
  

# Prerequisites
bash shell

# How to build

# How to start
--remove-orphans

# How to test
