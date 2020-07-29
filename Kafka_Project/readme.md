**Project Requirement**

The objective of this project is to develop a Data Pipeline addressing Data Ingestion, Data storage and Data Processing.

**Technologies Used**

Apache Kafka, Python

**Project Brief**

My goal was to automate the three main stages of Data Pipeline: Data Ingestion, Data Storage and Data Processing.
The prototype can process multiple data streams (obtained as API response from external data source: https://creativecommons.tankerkoenig.de/) at once.

**How to Run**
Run the forward_geo_coding to fecth the latitude and longitude information of the entered locations.
Run the producer to fetch the data from an api and store the messages int kafka buffer.
Run the consumer to consume the messages and store it into MongoDB database for further visualization
