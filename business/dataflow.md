# Dataflow Architecture
## Overview
The digital-footprint-watch system is designed to automate search and monitoring of personal digital footprints across multiple platforms. The following dataflow architecture outlines the flow of data through the system.

## External Data Sources
```
                                      +---------------+
                                      |  Social Media  |
                                      |  (Facebook,    |
                                      |   Twitter, etc.) |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Search Engines |
                                      |  (Google, etc.)  |
                                      +---------------+
                                             |
                                             |
                                             v
```
* Social media platforms (Facebook, Twitter, etc.)
* Search engines (Google, etc.)

## Ingestion Layer
```
                                      +---------------+
                                      |  Social Media  |
                                      |  (Facebook,    |
                                      |   Twitter, etc.) |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  API Connectors  |
                                      |  (Facebook API,  |
                                      |   Twitter API, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Web Scrapers    |
                                      |  (Google, etc.)  |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Message Queue  |
                                      |  (Apache Kafka,  |
                                      |   Amazon SQS, etc.)|
                                      +---------------+
```
* API connectors (Facebook API, Twitter API, etc.)
* Web scrapers (Google, etc.)
* Message queue (Apache Kafka, Amazon SQS, etc.)

## Processing/Transform Layer
```
                                      +---------------+
                                      |  Message Queue  |
                                      |  (Apache Kafka,  |
                                      |   Amazon SQS, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Data Processing |
                                      |  (Apache Spark,  |
                                      |   Apache Flink, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Data Transformation|
                                      |  (Apache Beam, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Auth Boundary    |
                                      |  (OAuth, etc.)     |
                                      +---------------+
```
* Data processing (Apache Spark, Apache Flink, etc.)
* Data transformation (Apache Beam, etc.)
* Auth boundary (OAuth, etc.)

## Storage Tier
```
                                      +---------------+
                                      |  Auth Boundary    |
                                      |  (OAuth, etc.)     |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Relational Database|
                                      |  (MySQL, etc.)     |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  NoSQL Database    |
                                      |  (MongoDB, etc.)   |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Data Warehouse    |
                                      |  (Amazon Redshift, |
                                      |   Google BigQuery, etc.)|
                                      +---------------+
```
* Relational database (MySQL, etc.)
* NoSQL database (MongoDB, etc.)
* Data warehouse (Amazon Redshift, Google BigQuery, etc.)

## Query/Serving Layer
```
                                      +---------------+
                                      |  Data Warehouse    |
                                      |  (Amazon Redshift, |
                                      |   Google BigQuery, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Query Engine     |
                                      |  (Apache Presto,  |
                                      |   Apache Hive, etc.)|
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  API Gateway      |
                                      |  (NGINX, etc.)     |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Auth Boundary    |
                                      |  (OAuth, etc.)     |
                                      +---------------+
```
* Query engine (Apache Presto, Apache Hive, etc.)
* API gateway (NGINX, etc.)
* Auth boundary (OAuth, etc.)

## Egress to User
```
                                      +---------------+
                                      |  Auth Boundary    |
                                      |  (OAuth, etc.)     |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Web Application  |
                                      |  (React, etc.)     |
                                      +---------------+
                                             |
                                             |
                                             v
                                      +---------------+
                                      |  Mobile Application|
                                      |  (iOS, Android, etc.)|
                                      +---------------+
```
* Web application (React, etc.)
* Mobile application (iOS, Android, etc.)

Auth boundaries are marked with `Auth Boundary` and are used to authenticate and authorize users before allowing access to the system.