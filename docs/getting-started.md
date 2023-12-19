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
2. Create and activate a virtual environment, 
then install the required Python packages that are listed in the `requirements.txt` file:


   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Download the HAI dataset from [here](https://github.com/icsdataset/hai/tree/master) 
and extract it into the `hai_dataset` folder.
In this project, the 21.03 version is used, 
so make sure that the files in the hai-21.03 folder are present and extracted.


4. Build the flink docker image:

   ```bash
   docker build -f pipeline/flink-dockerfile --tag pyflink:1.17.0 .
   ```


5. Start the pipeline using Docker Compose:

   ```bash
   docker compose -f pipeline/docker-compose.yaml up
   ```

   This will start all the necessary services and containers for the stream mining pipeline.
   (In rare cases Kafka may not start properly. If this happens, restart the container.)


6. Currently, you have to manually configure influxdb. 
To do this, open the influxdb UI in your browser at http://localhost:8086. 
Then, create an org `mema_org`, a bucket called `mema_bucket` and an admin called `admin` with password `admin1234`. 
Then, copy the token of the admin user and paste it into the `pipeline/telegraf/telegraf.conf` file 
at the influxdb output section to the `token` parameter. 
(Later you will be able to copy it into the `INFLUXDB_TOKEN` variable in the `.env` file. 
But for now, this option is not completed.)


7. Restart the telegraf in docker so that the token changes will be updated. 
(Alternatively you can restart the whole docker compose.)

   ```bash
   docker restart pipeline-telegraf-1
   ```


## Starting the Modules

After the pipeline is up and running, you can start the modules manually. To do this, follow these steps:
In the following steps everything should be done in the `marcell_drift_detection` folder, unless otherwise stated.

1. Connect to the pyspark jupyter notebook at 
http://localhost:8888/lab?token=<token-in-the-docker-pyspark-notebook-logs>. 
From the pyspark notebook logs you can directly open the link with the token as well. 
All the volumes should be mounted, so you should be able to find the `static_model_trainer.ipynb` notebook.
Run the notebook. It will create a new spark session. The training data will be loaded from the `hai_dataset` folder,
preprocessed, then the model will be trained and saved to the `models` folder under the name `base_model.joblib`.


2. Run the `data_streamer.ipynb` notebook. It will load the test data from the `hai_dataset` folder, 
and stream it to the kafka topic `hai-input`. 


3. Run the `stream_model_trainer.ipynb` notebook. It will load the data from the kafka topic `hai-input`, preprocess it
similarly to the static data preprocessing, then stream it to the kafka topic `hai-preprocessed`.


4. Run the `change_detector.ipynb` notebook. It will import the trained model saved by the static spark job.
Then, it will load the data from the kafka topic `hai-preprocessed`, and do the error rate based drift detection 
in the data and send the results to the kafka topic `hai-results`. It runs all the drift detection methods.


5. Run the `change_detector_multi_model.ipynb` notebook. It is quite similar to the previous notebook, 
but it will train a second model on the attack data, and will do the multimodel drift detection.


6. Checkout the Grafana dashboard at http://localhost:3000. You may log in with `admin`, `admin`. 
Connect to the influxdb v2 data source using the influxdb token that you created and put into the telegraf config file.
You can also check the `results` folder where you can find some plots.




