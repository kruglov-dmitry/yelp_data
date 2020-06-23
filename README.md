# TODO
- check bootstrap script
- check config ips
- Data Quality Assurance - aka e2e tests? - simple based on cassandra connector
- desicion log


# Repository layout
* **conf**      - contains external config files for docker containers
* **consumer**  - python module to consume data from kafka and publish it into cassandra
* **data**      - `yelp_dataset.tar` MUST be extracted into this folder (all bootstrap scripts expect it to be there)
* **deploy**    - docker-compose files for cassandra, kafka and spark
* **schemas**   - cassandra schema and deploy script
* **main.py**   - main driver program that orchestrate streaming logic with 

# Prerequisites
* bash shell
* python 2.7
* docker && docker-compose
* HOSTNAME environment variable are set within shell

# How to start
1. copy `yelp_dataset.tar` to ./data folder
```bash
cp yelp_dataset.tar ./data 
``` 
2. create virtual environment and install package with all dependencies:
```bash

```
3. start all services, upload data in Kafka and spawn spark streaming jobs to write data into Cassandra
```bash
./bootstrap.sh
```
Alternatively you may specify location of `yelp_dataset.tar`:
```bash
./bootstrap.sh -d /path/to/data/yelp_dataset.tar
```

## How to run streaming job
1. create virtualenv and install dependencies:
```bash
virtualenv venv && source ./venv/bin/activate
```
2. install requirements:
```bash
python setup.py develop
```
or
```bash
pip install -r requirements.txt 
```
3. edit `./consumer/1.cfg` if it necessary to adjust ip addresses of core services
3. Assuming data in corresponding kafka topics, list of supported topics: [business, review, user, checkin, tip] 
```bash
python main.py --cfg consumer/1.cfg --tid business
```

## How to run tests for streaming job
1. create virtualenv and install dependencies:
```bash
virtualenv venv && source ./venv/bin/activate
```
2. install tests requirements:
```bash
pip install -r test-requirements.txt 
```
3. execute tests 
```bash
tox
```


# Simplification
- kafka topics replication & partitions set to fixed values
- cassandra replication factor is set to 1
- number of nodes in setup decreased to have options to be able to run all setup within workstation
- events with mismatched schema are not published to corresponding errors topics
TODO:
- testing are very limited just to show example how it can be done

## Data schema modeling:
General consideration - Cassandra schema usually defined based on requirements of how user will query data.
As part of exercise tables in form of <entity_name> - is just snapshot of information as-is aka fact_tables:
* yelp_data.business, yelp_data.business_review_count
* yelp_data.review, yelp_data.review_reactions
* yelp_data.checkin
* yelp_data.tip, yelp_data.tip_compliment_count

Just to illustrate how desired tables can be derived I've added as example schema `yelp_data.business_by_location`
(without populating it though) with reversed index. 
It is designed to answer questions like: Show me businesseses by locations, with particular category and rating. 
and created dedicated table with appropriate indexes - i.e. PK will be geohash(lat, long): String, category, rating
NOTE: As a result data will be redundant (for every entry in business) we will multiplication factor for this table only
equatl to number of categories entries in original row.  

### Data adjustments

#### Business:
* postal code - initial intention was to cast it to integer, but look up at Wiki reveal that for some countries it may contains letters
* is_open -> from integer to boolean
* attributes -> from String to map (only programmatic filtering)
* hours -> from String to udt (only programmatic filtering)

#### Checkin:
* date (as space separated String) -> set<timestamp>

#### Tip:
* introduce artificial uuid based PK
* date (string) -> date

In real life stars computed to business, reviews and users will be resided in dedicated column family
or periodically re-computed in-mem cache that will be synced with cassandra table.

# Assumption
- demonstrate ops skills
- demonstrate familiarity with proposed tech stack
- demonstrate data modeling skills
- demonstrate spark specific data manipulation skills

# Troubleshooting
it usually helps to clean data folders from services:
```bash
rm -rf ./deploy/cassandra1/
rm -rf ./deploy/kafka_data/
rm -rf ./deploy/zoo_data/
```
in case of network issue may worth to check 1.cfg
additionally in `deploy/kafka.yml` - modify KAFKA_ADVERTISED_HOST_NAME

### Various
How to run cqlsh:
```bash
sudo docker exec -it cassandra1 cqlsh cassandra1
```
How to run pyspark:
```bash
sudo docker exec -it spark-master /spark/bin/pyspark
```