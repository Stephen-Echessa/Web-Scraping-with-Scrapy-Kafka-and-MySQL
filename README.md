# Real-Time Property Scraping with Scrapy, Kafka, and MySQL

## Project Overview

This project is designed to scrape property data from a real estate website in real-time and process it efficiently. The solution integrates **Scrapy**, **Apache Kafka**, and **MySQL** to automate the scraping process, handle streaming data, and store the results in a relational database. The deployment and scheduling of the spider are managed using **Scrapyd**, a powerful tool for running and managing Scrapy spiders.

## Technologies Used

### 1. **Scrapy**

**Scrapy** is a high-level web crawling and web scraping framework for Python. It is used in this project to:
- **Scrape Data:** Extract property details from the target website. Scrapy’s ability to handle complex scraping tasks and manage requests efficiently makes it ideal for this project.
- **Handle Pagination:** Navigate through multiple pages to gather comprehensive data.

### 2. **Apache Kafka**

**Apache Kafka** is a distributed event streaming platform used for:
- **Event Streaming:** Kafka enables the real-time streaming of data. After the data is scraped by Scrapy, Kafka streams it to different consumers, ensuring that data processing is decoupled from data collection.
- **Data Integration:** Kafka acts as a buffer between the scraping process and the data storage, allowing for smooth integration and real-time data handling.

### 3. **MySQL**

**MySQL** is a widely-used relational database management system employed to:
- **Store Data:** Persistently store the scraped data in a structured format. MySQL’s robust querying capabilities and data management features make it suitable for handling and retrieving property data.
- **Ensure Data Integrity:** Provide reliable storage with support for transactions and data integrity checks.

### 4. **Scrapyd**

**Scrapyd** is an open-source service for running and scheduling Scrapy spiders. It is used to:
- **Automate Scraping:** Schedule the execution of spiders at regular intervals to ensure continuous data collection.
- **Manage Spiders:** Deploy and manage multiple spiders, monitor their execution, and handle their scheduling through a simple API.

## Project Setup and Workflow

### 1. Install Required Libraries

Install Python libraries for Scrapy, Kafka, MySQL, and Scrapyd:

```bash
pip install scrapy kafka-python mysql-connector-python scrapyd-client
```

### 2. Set Up Scrapy Project

Create and configure Scrapy project to scrape property data:

```bash
scrapy startproject property_scraper
```

Define spider in property_scraper/spiders/property_spider.py to extract relevant property details, handle pagination, and process the data.

### 3. Integrate Kafka

Set up Kafka to handle event streaming:

  - Kafka Producer: Send the scraped data to a Kafka topic.
  - Kafka Consumer: Read from the Kafka topic and insert data into MySQL.

Example Kafka producer and consumer scripts are included to illustrate how to handle data streaming and processing.

### 4. Configure MySQL
Create a MySQL database and table to store the scraped property data. Use MySQL commands or a GUI tool to define your database schema.

### 5. Deploy with Scrapyd

Install and configure Scrapyd to manage and schedule your spiders:

```bash
pip install Scrapyd
```

Start Scrapyd Service:

```bash
scrapyd
```

Deploy Your Spider:

Use scrapyd-client to deploy your spider:

```bash
scrapyd-deploy
```

### 6. Schedule Scraping Jobs

Use Scrapyd’s REST API to schedule your spider or set up a cron job to trigger it at regular intervals.
API Scheduling Example:

```bash

curl -X POST "http://localhost:6800/schedule.json" \
     -d "project=your_project_name" \
     -d "spider=your_spider_name" \
     -d "property_type=apartment" \
     -d "payment_type=rent"
```

Cron Job Example:

```bash
0 2 * * * curl -X POST "http://localhost:6800/schedule.json" -d "project=your_project_name" -d "spider=your_spider_name" -d "property_type=apartment" -d "payment_type=rent"
```

## Running the Project

  - Start Kafka and Scrapyd services.
  - Deploy your Scrapy spider using scrapyd-deploy.
  - Schedule the spider using Scrapyd’s API or a cron job.
  - Monitor the Kafka consumer to process and store the data into MySQL.

## Troubleshooting
  - Connection Issues: Ensure that all services (Scrapyd, Kafka, MySQL) are up and running and that there are no connectivity issues.
  - Deployment Errors: Check Scrapyd logs for any errors during deployment.
  - Data Processing Problems: Verify Kafka consumer code and MySQL connection settings.
