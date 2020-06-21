#!/usr/bin/env bash
CASSANDRA_CONTAINER_NAME=cassandra1
SCHEMA_FOLDER=./schemas/
SCHEMA_FOLDER_IN_DOCKER=/schemas/

DOCKER_EXEC="sudo docker exec -it ${CASSANDRA_CONTAINER_NAME} cqlsh ${CASSANDRA_CONTAINER_NAME} -f "

for filename in ${SCHEMA_FOLDER}*.cql; do
    schema_file=${filename##*/}
    echo ${DOCKER_EXEC} ${SCHEMA_FOLDER_IN_DOCKER}${schema_file}
done
