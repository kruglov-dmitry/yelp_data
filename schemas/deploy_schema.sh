#!/usr/bin/env bash
CASSANDRA_HOST_NAME=cassandra1
SCHEMA_FOLDER=/schemas/

for filename in ${SCHEMA_FOLDER}*.cql; do
    schema_file=${filename##*/}
    cqlsh ${CASSANDRA_HOST_NAME} -f ${SCHEMA_FOLDER}${schema_file}
done

