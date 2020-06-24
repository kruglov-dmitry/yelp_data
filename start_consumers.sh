#!/usr/bin/env bash
TOPICS=(business review user checkin tip)

for topic_name in "${TOPICS[@]}"
do
	python main.py --cfg 1.cfg --tid ${topic_name} &
done
