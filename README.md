# Repository layout
* conf      - contains external config files for docker containers
* consumer  - python module to consume data from kafka and publish it into cassandra
* data      - yelp_dataset.tar MUST be extracted into this folder (all bootstrap scripts expect it to be there)
* deploy    - docker-compose files for cassandra, kafka and spark
* schemas   - cassandra schema and deploy script


# Simplification
- kafka topics replication & partitions set to fixed values
- cassandra replication factor is set to 1
- number of nodes in setup decreased to have options to be able to run all setup within workstation

# Assumption
- demonstrate ops skills
- demonstrate familiarity with proposed tech stack
- demonstrate data modeling skills
- demonstrate spark specific data manipulation skills

## Data schema modeling:
General consideration - Cassandra schema usually defined based on requirements of how user will query data.
As part of exersise tables in form of <entity_name> - is just snapshot of information as-is aka fact_tables:
* yelp_data.business, yelp_data.business_review_count
* yelp_data.review, yelp_data.review_reactions
* yelp_data.checkin
* yelp_data.tip, yelp_data.tip_compliment_count

Just to illustrate how desired tables can be derived I've added as example schema `yelp_data.business_by_location`
(without populating it though). 
If we need to answer questions like: get businesses by locations, with particular category and rating. 
and created dedicated table with appropriate indexes - i.e. PK will be geohash(lat, long): String, category, rating

as a result data will be redundant (for every entry in business) we will have number of categories entries in  


I made assumptions that we may need to answer efficiently these kind of questions:
- 

Data modifications in comparison to raw data:

  

Business:
- postal code - initial intention was to cast it to integer, but look up at Wiki reveal that for some countries it may contains letters
- is_open - from integer to boolean
- attributes to map (only programmatic filtering)
- hours - to udt (only programmatic filtering)

Counters for business, reviews, tip - should be updated independent from main records
- stars to dedicated column family?

Checkin:
- date (as space separated String) -> set<timestamp>

Reviews:
- stars to dedicated column family?

Tip:
- introduce artificial uuid based PK
- date (string) -> date

User:
- average_stars - to dedicated column family?


Reverse indexes:
category -> business_ids + hours + location (lat, long)
  

# Prerequisites
bash shell

# How to build

# How to start
--remove-orphans

# How to test



# TODO
setup:
- schema in cassandra
Spark streaming job => Kafka => Cassandra
Data Quality Assurance - aka e2e tests?
ETL(?) logic autotests?
add last_review first - for schema