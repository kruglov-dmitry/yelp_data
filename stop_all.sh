#!/usr/bin/env bash
sudo docker stop zookeeper kafka spark-master spark-worker-1 cassandra1
rm -rf ./deploy/cassandra1/*
rm -rf ./deploy/kafka_data/*
rm -rf ./deploy/zoo_data/*