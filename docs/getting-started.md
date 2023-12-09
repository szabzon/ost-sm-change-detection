# Getting Started with OST-SM change detection project by team MEMA

**Important:** This project documentation is for the actual stream mining pipeline and modules. Emma, one of our team members, has created a separate pipeline for the staic/batch data analysis. You can find the documentation for that [here]().

This guide will walk you through the steps to get started with theg project. The project includes a pipeline that can be run using Docker Compose, as well as certain modules that can be started manually.

## Prerequisites

Before you begin, make sure you have the following installed on your machine:

- Docker
- Docker Compose
- Python 3.10 or higher

## Setting up the Pipeline

To set up the pipeline, follow these steps:

1. Clone the project repository:

   ```bash
   git clone https://github.com/szabzon/ost-sm-change-detection.git
   ```

2. Navigate to the pipeline directory:

   ```bash
   cd pipeline
   ```

3. Start the pipeline using Docker Compose:

   ```bash
   docker-compose up -d
   ```

   This will start all the necessary services and containers for the stream mining pipeline.

4. Currently you have to manually configure influxdb. To do this, open the influxdb UI in your browser at http://localhost:8086. Then, create an org `mema_org`, a bucket called `mema_bucket` and an admin called `admin` with password `admin1234`. Then, copy the token of the admin user and paste it into the `telegraf.conf` file. (Later you will be able to copy it into the `INFLUXDB_TOKEN` variable in the `.env` file. But for now, this option is not working.) 

TODO: add correct cli commands.
You can also do this by running the following commands in the influxdb CLI:

   ```bash
   influx
   > create user admin with password 'admin1234' with all privileges
   > create database mema_bucket
   > create user telegraf with password 'telegraf1234'
   > grant all on mema_bucket to telegraf
   ```

## Starting Modules Manually

In addition to the pipeline, there are certain modules that need to be started manually. Follow these steps to start the modules:

This section will be updated as soon as the modules are ready.

That's it! You have successfully set up the stream mining project and started the pipeline and modules. You can now start processing streams and analyzing data.
