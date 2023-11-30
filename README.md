# Project-Real-time-Sentiment-Analysis


- docker-compose -f zk-single-kafka-single.yml up -d
- docker-compose -f zk-single-kafka-single.yml ps
- docker exec -it kafka1 /bin/bash
- kafka-topics --version
- kafka-topics --create --topic twitter --bootstrap-server localhost:9092
- kafka-topics --describe --topic twitter --bootstrap-server localhost:9092
- sudo apt update
- sudo apt install python3-pip
- pip install kafka-python
- python3 producer.py
