#!/bin/bash -x

KAFKA_CONTAINER_NAME=kafka
DOCKER_EXEC="sudo docker exec -it ${KAFKA_CONTAINER_NAME} /opt/kafka/bin/"
REPLICATION_FACTOR="--replication-factor 1"
PARTITION_FACTOR="--partitions 10"
CREATE_KAFKA_TOPIC="${DOCKER_EXEC}kafka-topics.sh --create --bootstrap-server ${KAFKA_CONTAINER_NAME}:9092 ${REPLICATION_FACTOR} ${PARTITION_FACTOR} --topic "

TOPICS=(business review user checkin tip)

for topic_name in "${TOPICS[@]}"
do
	${CREATE_KAFKA_TOPIC} ${topic_name}
done
