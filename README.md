﻿# Project-Real-time-Sentiment-Analysis


- docker-compose up --build -d
- docker-compose -f zk-single-kafka-single.yml ps
- docker exec -it kafka1 /bin/bash
- kafka-topics --version
- kafka-topics --create --topic twitter --bootstrap-server localhost:9092
- kafka-topics --describe --topic twitter --bootstrap-server localhost:9092
- sudo apt update
- sudo apt install python3-pip -Y
- pip install -r requirements.txt
- python3 producer.py
- In another tab run python3 con.py
- 
