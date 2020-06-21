#!/usr/bin/env bash
########################################################################################################################
# The script runs a docker containers with kafka, spark and cassandra.
# Parameters are
# -h= / --help=         file name of archive with yelp dataset. Default is data/yelp_dataset.tar
# -d= / --data=         file name of archive with yelp dataset. Default is data/yelp_dataset.tar
#
#
# Example usage:
#    ./bootstrap.sh -d /path/to/data/yelp_dataset.tar
#    ./bootstrap.sh
#
# Notes:
#       Depending on host system and its configuration you may or not require root privilege.
#       Those script assume users who execute script are within sudo group.
#
########################################################################################################################

usage() {
    echo "This script must be run with super-user privileges."
	echo -e "\nUsage:\n $(basename "$0") [options] [-d path-to-tar] \n"
	echo -e "-h | --help                    print this usage and exit"
	echo -e "-d | --data some_file.tar      instead of default location will load data from provided archive"
}

start_all_services() {
    echo "1st stage - Starting all services..."
    sudo docker-compose -f deploy/kafka.yml up -d
    sudo docker-compose -f deploy/spark.yml up -d
    sudo docker-compose -f deploy/cassandra.yml up -d
}

setup_all_services() {
    echo "2nd stage - setup all services"
    ./create_kafka_topics.sh
    ./create_cassandra_schema.sh
    ./start_consumer.sh
}

push_data_to_kafka() {
    echo "3rd stage - publish data into kafka"

    if [[ ! -f "${YELP_DATA_ARCHIVE}" ]]; then
        echo "Error - ${YELP_DATA_ARCHIVE} file does not exist!"
        exit 13
    fi

    tar xfvz YELP_DATA_ARCHIVE -C ./data/

    # FIXME
    KAFKA_CONTAINER_NAME=kafka
    DOCKER_EXEC="sudo docker exec -it ${KAFKA_CONTAINER_NAME} /opt/kafka/bin/"
    RAW_DATA=/raw_data/

    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic business < /raw_data/yelp_academic_dataset_business.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic checkin < /raw_data/yelp_academic_dataset_checkin.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic review < /raw_data/yelp_academic_dataset_review.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic user < /raw_data/yelp_academic_dataset_user.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic tip < /raw_data/yelp_academic_dataset_tip.json
}

YELP_DATA_ARCHIVE=./data/yelp_dataset.tar

#
#               Main
#

while [[ $# -gt 0 ]]
do
    key="$1"

    case ${key} in
        -h|--help)
                usage
                exit 0
                ;;
        -d|--data)
                YELP_DATA_ARCHIVE="$2"
                shift
                ;;
        *)
                # unknown option
                ;;
    esac
    shift # past argument or value
done

echo "Going to push data from ${YELP_DATA_ARCHIVE}"

start_all_services
setup_all_services
push_data_to_kafka