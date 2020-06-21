#!/usr/bin/env bash
CASSANDRA_CONTAINER_NAME=cassandra1
SCHEMA_FOLDER_IN_DOCKER=/schemas/

sudo docker exec -it ${CASSANDRA_CONTAINER_NAME} ${SCHEMA_FOLDER_IN_DOCKER}/deploy_schema.sh

