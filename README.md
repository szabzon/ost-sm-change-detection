**Data Science Project: Error Rate-Based Change Detection**

**Overview**
This data science project focuses on error rate-based change detection using the HAI dataset. The project involves loading the dataset from a CSV file, streaming it row by row to Kafka, applying various change detection algorithms, saving the data and results to InfluxDB, and visualizing both the data and results in Grafana.

**Architecture**
In the image below, you can see the architecture of the project.
![Architecture](<architecture (1).png>)


**Project Structure**

Please read the project structure documentation to get a better understanding of the project.


**Algorithms**

The following error rate-based change detection algorithms are implemented.

1. KSWin
2. PageHinkley
3. ADWIN
4. EDDM

**Data Flow**

Static Pipeline
Load HAI training dataset from CSV.
Apply preprocessing (Feature selection, splitting, and other data prep.)
Train and evaluate models (Random Forest)
Save models to disk.
Stream Pipeline
Load HAI dataset from CSV.
Stream data row by row to Kafka.
Do preprocessing (Feature selection, splitting, and other data prep.)
Apply change detection algorithms.
Save data and results to InfluxDB.
Visualize data and results in Grafana.

**Difficulties:**

We endeavored to establish a connection between Kafka and Spark for data preprocessing, investing a substantial amount of time in experimenting with various configurations. Despite our efforts, we encountered challenges and were unable to achieve a successful connection. While Spark performed seamlessly in a stand-alone setting, integrating it with Kafka proved unsuccessful. Each attempt resulted in an error, signaling the failure to establish a successful connection between Kafka and Spark. The details of our attempts are documented in the repository, providing a historical record of our efforts in trying to make the connection work.

**Contributions:**

To make it work we were working together as a team in each part including Docker compose file, Kafka setup and configuration for ingesting data as stream, Kafka data ingestion as stream​, connecting Spark with Kafka​, InfluxDB setup with Python inside Kafka Consumer, TIG stack configuration and setup. And individually we implemented our own algorithms.
