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

self_check() {
    if [[ $? -eq 0 ]]; then
        echo OK
    else
        echo "Error's during last command processing, exiting..."
        exit 13
    fi
}

start_all_services() {
    export HOSTNAME
    echo "1st stage - Starting all services..."
    sudo docker-compose -f deploy/kafka.yml up -d
    sudo docker-compose -f deploy/spark.yml up -d
    sudo docker-compose -f deploy/cassandra.yml up -d
    # NOTE: to wait a bit and allow cassandra to start
    sleep 5
    self_check
}

setup_all_services() {
    echo "2nd stage - setup all services"
    ./create_kafka_topics.sh
    ./create_cassandra_schema.sh
    self_check
}

push_data_to_kafka() {
    echo "3rd stage - publish data into kafka"

    if [[ ! -f "${YELP_DATA_ARCHIVE}" ]]; then
        echo "Error - ${YELP_DATA_ARCHIVE} file does not exist!"
        exit 13
    fi

    tar xfvz ${YELP_DATA_ARCHIVE} -C ./data/
    self_check
    # NOTE: to wait a bit and allow docker to sync
    sleep 5

    # FIXME
    KAFKA_CONTAINER_NAME=kafka
    DOCKER_EXEC="sudo docker exec -i ${KAFKA_CONTAINER_NAME} /opt/kafka/bin/"
    RAW_DATA=/raw_data/

    echo "3rd stage - about to start publish json into kafka - in total it will take around 10 minutes..."

    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic business < ./data/yelp_academic_dataset_business.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic checkin < ./data/yelp_academic_dataset_checkin.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic review < ./data/yelp_academic_dataset_review.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic user < ./data/yelp_academic_dataset_user.json
    ${DOCKER_EXEC}/kafka-console-producer.sh --broker-list kafka:9092 --topic tip < ./data/yelp_academic_dataset_tip.json

    self_check

    echo "3rd stage - Done"
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