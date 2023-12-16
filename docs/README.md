# Data Science Project: Error Rate-Based Change Detection

## Overview

This data science project focuses on error rate-based change detection using the HAI dataset. The project involves loading the dataset from a CSV file, streaming it row by row to Kafka, applying various change detection algorithms, saving the data and results to InfluxDB, and visualizing both the data and results in Grafana.

## Architecture
In the image below, you can see the architecture of the project.

![Architecture](architecture.png)

## [Project Structure](project-structure.md)
Please read the project structure documentation to get a better understanding of the project.

## [Getting Started](getting-started.md)
This section is very important. Please read it carefully to get started with the project 
and to understand how the pipeline works.

## Flink situation
**Please read**

This is a rather interesting situation.

In the main pipeline, which is the streaming pipeline, there are a few steps that do real-time processing of the data.
These steps are the following:
- Stream preprocessing
- Change detection

These steps should be done using a stream processing framework, such as Flink. 
I chose Flink because it is truly a stream processing framework (unlike spark streaming), 
and it offers exactly once guarantees (unlike Storm). 

I configured Flink in the docker-compose file, and I also created a dockerfile for PyFlink.
I created PyFlink jobs for the above-mentioned steps.

However, this is where the problem comes in. 
As you may know, Flink is a Java / Scala framework, and it is not very easy to use it with Python.
PyFlink is rather new, and therefore it is not a very mature solution. 
There are a lot of extra configuration steps, the image is not out of the box, 
there are dependencies that are needed to be built, installed and sourced manually. 
Volumes were needed to be mounted, etc.
I went through all of this, and I managed to get the PyFlink image to work.
It is up and running, and it would be able to run JAR files. 

When running python jobs, however, error came after another. 
After spending many days on this I got closer to the solution, but I still couldn't get it to work.
I asked for help and one of my teachers, Peter Kiss was kind enough to help me out. 
He helped a lot, which I am very grateful for. 
Unfortunately though, we couldn't get it fully working and I had to give up on it to be able to finish the project.

So what I ended up doing is the following:
- I kept the Flink in the pipeline and the PyFlink jobs in the Flink folder
- But I also created regular Python notebooks that do the same thing as the PyFlink jobs.

By the way, if you are someone who has experience with PyFlink, or you know someone who does, please let me know, 
because I would really like to get it working, regardless of the project.

## Algorithms

The following error rate-based change detection algorithms are implemented.

#### 1. DDM

#### 2. HDDM-W

#### 3. Basic window-based drift detection

#### 4. ECDD

####  +1. Multi-model drift detection and adoption



## Data Flow

### Static Pipeline
1. Load HAI training dataset from CSV.
2. Apply preprocessing (Feature selection, splitting, and other data prep.)
3. Train and evaluate models (Random Forest)
4. Save models to disk.

### Stream Pipeline
1. Load HAI dataset from CSV.
2. Stream data row by row to Kafka.
3. Do preprocessing (Feature selection, splitting, and other data prep.)
4. Apply change detection algorithms (Flink and/or Python).
5. Save data and results to InfluxDB.
6. Visualize data and results in Grafana. (Also, create plots in Python.)

## References

- [HAI Dataset](link-to-hai-dataset)
- [Kafka Documentation](link-to-kafka-doc)
- [Flink Documentation](link-to-flink-doc) 
- [InfluxDB Documentation](link-to-influxdb-doc)
- [Grafana Documentation](link-to-grafana-doc)
- [Spark Documentation](link-to-spark-doc)
- [Change Detection Algorithms](link-to-change-detection-algorithms)


