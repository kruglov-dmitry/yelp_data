#!/usr/bin/env bash
sudo docker stop zookeeper kafka spark-master spark-worker-1 cassandra1
sudo rm -rf ./deploy/cassandra1/*
sudo rm -rf ./deploy/kafka_data/*
sudo rm -rf ./deploy/zoo_data/*