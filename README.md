# Real-Time Sentiment Analysis Project Architecture

## Overview
This document presents the architecture and steps for setting up a real-time sentiment analysis project. The project aims to collect, process, and visualize sentiment data from social media platforms, with a focus on Twitter. It utilizes a combination of Docker, Kafka, Python, Spark, MongoDB, and Django to create a scalable and powerful system for monitoring customer sentiment trends in real-time.

![Real-Time Sentiment Analysis Architecture](architecture.png)

## Components

### 1. Docker Containers
Docker containers provide isolation for various project components, allowing for easy deployment and scalability. They encapsulate Kafka, Spark, Python scripts, and MongoDB, ensuring efficient resource management.

### 2. Kafka
Kafka acts as a central message broker in the architecture, ingesting data from various sources and streaming it downstream. It provides reliable data transport and real-time processing capabilities.

### 3. Twitter Data Collector
A Python script serves as the Twitter data collector. It continuously gathers real-time Twitter data, including tweets, usernames, and metadata, and sends this data to Kafka for further processing.

### 4. Spark Processing
Apache Spark plays a crucial role in the architecture, consuming data from Kafka. It performs sentiment analysis using libraries like TextBlob, allowing for the classification of tweets into positive, negative, or neutral sentiments. Additionally, Spark extracts mentions of competitors from the tweets.

### 5. MongoDB
MongoDB serves as the database for storing processed sentiment data. Python scripts consume data from Kafka, process it further if needed, and store it in MongoDB for easy retrieval and analysis.

### 6. Django Web Application
A Django web application provides the user interface for real-time sentiment analysis insights. This component connects to MongoDB, retrieves sentiment data, and presents it through interactive visualizations, enabling users to monitor customer sentiment trends effectively.

## Data Flow

The architecture's data flow ensures the seamless processing of real-time sentiment data:

1. Twitter data is continuously collected and ingested into Kafka, where it is made available for processing.
2. Apache Spark processes the incoming data, performing sentiment analysis and competitor mention extraction.
3. Processed data is sent to another Kafka topic for further consumption and analysis.
4. Python scripts consume, process, and store data in MongoDB, making it accessible for query and analysis.
5. The Django web application connects to MongoDB and displays real-time sentiment insights, allowing users to interact with the data and gain valuable insights.

## Steps to Set Up the Project

Follow these steps to set up and run the real-time sentiment analysis project:

1. Initiate Docker Compose and start the defined containers using the command `docker-compose up --build -d`.

2. Verify the status and information of the containers with the command `docker-compose ps`.

3. Update Ubuntu packages to ensure you have the latest information about available packages: `sudo apt update`.

4. Install Python 3 and pip, which are essential for managing Python package dependencies: `sudo apt install python3-pip -y`.

5. Install project dependencies by running `pip install -r requirements.txt`.

6. Execute the Twitter data collection script with `python3 producer_TwitterData.py`. This script collects real-time Twitter data and sends it to Kafka.

7. Run the Kafka consumer/producer script with `python3 kafka_consumer_producer.py`. This script consumes data from Kafka, performs additional processing, and sends the results to another Kafka topic.

8. Consume Kafka data, process it, and store it in MongoDB by running `python3 kafka_consumer_MangoDB`. This step may involve batch processing of data.

9. Verify that the data has been successfully appended to MongoDB by querying the database.

10. Create a Django web application for front-end visualization by navigating to the `Twitter_Django` folder and running the application with `python3 manage.py runserver`.

11. Ensure that all components are running correctly, and access the Django web application to view and interact with real-time sentiment insights.

This architecture provides a comprehensive solution for real-time sentiment analysis, enabling businesses to monitor and analyze customer sentiment on social media platforms effectively.

## Project Output
Please add the output image or screenshots of the project's real-time sentiment analysis dashboard here:

![Real-Time Sentiment Analysis Dashboard](dashboard.png)

In the image above, you can see the real-time sentiment analysis dashboard generated by the Django web application. It provides interactive visualizations and insights into customer sentiment trends on social media platforms, allowing businesses to make data-driven decisions and monitor their online reputation.
