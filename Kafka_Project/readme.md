The objective of this project is to develop a Data Pipeline.
My goal is to automate the three main stages of Data Pipeline: Data Ingestion, Data Storage and Data Processing.
The prototype can process multiple data streams (obtained as API response from external data source) at once.

Run the producer to fetch the data from an api and store the messages int kafka buffer.
Run the consumer to consume the messages and store it into MongoDB database for further visualization
