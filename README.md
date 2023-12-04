# Setting Up a Real-Time Sentiment Analysis Project

## Overview

This document provides a step-by-step guide on how to set up and run a real-time sentiment analysis project. The project involves using Docker, Kafka, Python, Spark, MongoDB, and Django to collect, process, and visualize sentiment data in real-time. Follow these instructions to create a fully functional real-time sentiment analysis pipeline.

## Prerequisites

Before you begin, ensure that you have the following prerequisites in place:

- Docker installed and configured
- Python 3 and pip installed
- Access to the required libraries and packages (specified in `requirements.txt`)
- Understanding of Docker Compose
- Familiarity with Kafka, Spark, MongoDB, and Django

# Real-Time Sentiment Analysis Architecture

## Overview

This architecture enables real-time sentiment analysis by collecting, processing, and visualizing data from social media platforms like Twitter.

## Components

### 1. Docker Containers

Docker containers provide isolation for Kafka, Spark, Python scripts, and MongoDB components, ensuring easy deployment and scalability.

### 2. Kafka

Kafka acts as a central message broker, ingesting data from various sources and reliably streaming it downstream.

### 3. Twitter Data Collector

A Python script collects real-time Twitter data, including tweets, usernames, and metadata, and sends it to Kafka.

### 4. Spark Processing

Apache Spark consumes data from Kafka, performs sentiment analysis using libraries like TextBlob, and extracts competitor mentions.

### 5. MongoDB

MongoDB stores processed sentiment data. Python scripts consume Kafka data, process it, and store it in MongoDB.

### 6. Django Web Application

A Django web app connects to MongoDB, retrieves sentiment data, and presents real-time insights through interactive visualizations.

## Data Flow

1. Twitter data is continuously collected and ingested into Kafka.
2. Spark processes data, performs sentiment analysis, and extracts competitor mentions.
3. Processed data is sent to another Kafka topic.
4. Python scripts consume, process, and store data in MongoDB.
5. Django web app connects to MongoDB and displays real-time sentiment insights.

## Conclusion

This architecture offers a comprehensive solution for real-time sentiment analysis, utilizing Docker, Kafka, Spark, MongoDB, and Django to create a scalable and powerful system for monitoring social media sentiment trends.


## Step-by-Step Guide

- **docker-compose up --build -d**: This command initiates Docker Compose to build and start the defined containers in detached mode. It launches the various components required for the project, such as Kafka, Spark, and MongoDB, in separate containers.

- **docker-compose ps**: After the containers are running, this command displays the status and information of all containers managed by Docker Compose. It allows you to verify that the containers are up and running.

- **sudo apt update**: This command updates the package list on your Ubuntu system, ensuring that you have the latest information about available packages.

- **sudo apt install python3-pip -y**: It installs the Python 3 package manager (pip) on your system. Pip is used to manage Python package dependencies.

- **pip install -r requirements.txt**: This command installs the Python packages listed in the requirements.txt file. These packages typically include libraries and modules required for the project, such as Kafka libraries, Spark dependencies, and more.

- **python3 producer_TwitterData.py**: You run the Python script producer_TwitterData.py. This script likely collects Twitter data and sends it to a Kafka topic, acting as a Kafka producer.

- **python3 kafka_consumer_producer.py**: This script functions as a Kafka consumer that consumes data from the Kafka topic (where it was produced by the previous step) and performs additional processing, possibly using Spark. It then sends the processed data back to another Kafka topic, acting as both a Kafka consumer and producer.

- **python3 kafka_consumer_MangoDB**: In this step, Kafka data is consumed by another script, and the data is further processed. This processed data is then sent to a MongoDB database. This step might involve batch processing of the data.

Check with data in MongoDB is appended: After the data is sent to MongoDB, you should check whether the data has been successfully appended to the MongoDB database. You can query the database to ensure the data is there.

Creating the Django for front-end visualization by using the data from MongoDB: This step involves creating a Django web application for front-end visualization. The Django application connects to the MongoDB database, retrieves the data, and uses it to generate visualizations or present it on a web interface for users to interact with.
