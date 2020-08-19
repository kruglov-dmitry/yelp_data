# Solution overview:
Data from [Yelp dataset](https://www.yelp.com/dataset/) - json files - are loaded by kafka console-producers into appropriate kafka topics.
Python kafka consumers, based on spark structured streaming read those data, 
shape it according to cassandra schema (using advanced built-in types: [counter](https://github.com/kruglov-dmitry/yelp_data/blob/master/cql_schemas/user.cql#L10), [set](https://github.com/kruglov-dmitry/yelp_data/blob/master/consumer/transform/business.py#L16), [map](https://github.com/kruglov-dmitry/yelp_data/blob/master/consumer/transform/business.py#L22),
 as well as [UDT](https://github.com/kruglov-dmitry/yelp_data/blob/master/consumer/schemas/Business.py#L3) - user defined types, parsing and [typecasting](https://github.com/kruglov-dmitry/yelp_data/blob/master/consumer/transform/user.py#L38))
and write it in appropriate tables.

# Decision log
- Initial attempt to use confluent's kafka connect - miserably failed,
for some reason it stop publish messages into kafka topic after approximately 10k msg
- additionally kafka connect wrap each event into nested structure 
- console-producers was able to publish all messages in less than 10 minutes
- kafka topics replication & partitions set to fixed values
- cassandra replication factor is set to 1
- number of nodes in setup decreased to have options to be able to run all setup within workstation
- events with mismatched schema are not published to corresponding errors topics
- testing are very limited just to demonstrate how it can be done
- for approach result validation and data exploratory analysis check section [How to get number of businesses per category from cassandra table](how-to-run-tests-for-streaming-job)

# Repository layout
* **conf**      - contains external config files for docker containers
* **consumer**  - python module to consume data from kafka and publish it into cassandra
* **data**      - `yelp_dataset.tar` MUST be extracted into this folder (all bootstrap scripts expect it to be there)
* **deploy**    - docker-compose files for cassandra, kafka and spark
* **cql_schemas**   - cassandra schema and deploy script
* **main.py**   - driver program that orchestrate streaming logic 
* **bootstrap.sh** - deploy and start all services
* **stop_all.sh** - stop all docker containers and CLEAN container's data and metadata  
* **start_consumers.sh** - start all streaming jobs as background processes  

# Prerequisites
* java 8 (see at the bottom how to use `sdk` tool to add additional java version)
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
virtualenv -p /usr/bin/python2.7 venv && source ./venv/bin/activate
python setup.py install
```
2.5 update value of `KAFKA_ADVERTISED_HOST_NAME` in deploy/kafka.yml to be ip address 
(not loopback, not 127.0.0.1). It will work as it is in Linux, but not at Mac.
or alternatively you may explicitly export HOSTNAME:
```bash
export HOSTNAME
```
3. start all services, upload data in Kafka and spawn spark streaming jobs to write data into Cassandra
```bash
./bootstrap.sh
```
Alternatively you may specify location of `yelp_dataset.tar`:
```bash
./bootstrap.sh -d /path/to/data/yelp_dataset.tar
```
NOTE: sometimes cassandra take more time to start properly, in this case it necessary to wait for several minutes
and just re-start ./bootstrap.sh

## How to run single streaming job
1. create virtualenv and install dependencies:
```bash
virtualenv -p /usr/bin/python2.7 venv && source ./venv/bin/activate
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

## How to run all streaming jobs
```bash
./start_consumers.sh
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

# How to get number of businesses per category from cassandra table
In case you want to run it with this module available, assuming you already install all requirements:
```bash
cd consumer && ./make_dist.sh
sudo docker exec -it spark-master /spark/bin/pyspark \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0,com.datastax.spark:spark-cassandra-connector_2.11:2.4.0 \
--conf spark.cassandra.connection.host=192.168.0.9 \
--conf spark.cassandra.connection.port=9042 \
--conf spark.cassandra.output.consistency.level=ONE \
--py-files /consumer/dependencies.zip
```
```python
from pyspark.sql.functions import explode, col, countDistinct
df = spark.read\
.format("org.apache.spark.sql.cassandra")\
.options(table="business", keyspace="yelp_data")\
.load()
df.printSchema()
df.count()
df = df.select(col("business_id"), explode("categories").alias("category"))
df = df.groupBy("category").agg(countDistinct("business_id"))
df.show()
```

## Data schema modeling:
General consideration - Cassandra schema usually defined based on requirements of how user will query data.
As part of exercise tables in form of <entity_name> - is just snapshot of information as-is aka fact_tables:
* yelp_data.business, yelp_data.business_review_count
* yelp_data.review, yelp_data.review_reactions
* yelp_data.checkin
* yelp_data.tip, yelp_data.tip_compliment_count

Just to illustrate how desired tables can be derived I've added as example schema `yelp_data.business_by_location`
(without populating it though) with reversed index. 
It is designed to answer questions like: Show me businesses by locations, with particular category and rating. 
and created dedicated table with appropriate indexes - i.e. PK will be geohash(lat, long): String, category, rating
NOTE: As a result data will be redundant (for every entry in business) we will multiplication factor for this table only
equal to number of categories entries in original row.  

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
or periodically re-computed in in-mem cache that will be synced with cassandra table.

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
sudo docker exec -it spark-master /spark/bin/pyspark \
--packages org.apache.spark:spark-sql-kafka-0-10_2.11:2.4.0,com.datastax.spark:spark-cassandra-connector_2.11:2.4.0 \
--conf spark.cassandra.connection.host=192.168.0.9 \
--conf spark.cassandra.connection.port=9042 \
--conf spark.cassandra.output.consistency.level=ONE
```

How to install java 8:
```bash
curl -s "https://get.sdkman.io" | bash
source "$HOME/.sdkman/bin/sdkman-init.sh"
sdk install java 8.0.252-amzn
sdk use java 8.0.252-amzn
```

time for pushing biggest file into kafka:
```bash
time kafka-console-producer.sh --broker-list kafka:9092 --topic review < /raw_data/yelp_academic_dataset_review.json 
real	5m40.304s
user	2m2.007s
sys	1m7.300s
```

#### some usefull commands
```bash
export PYSPARK_PYTHON=python3
export PYTHONPATH=$PYTHONPATH:/consumer/
pyspark --py-files dependencies.zip
```
