# Project Structure

The project is structured as follows:
In the root folder are 4 folders:
- `docs`: contains the documentation of the project
- `hai_dataset`: contains the HAI dataset
- `marcell_drift_detection`: contains all the modules and codes for the stream mining pipeline
- `pipeline`: contains the docker-compose file for the pipeline and the dockerfile for the flink image 
along with some configuration files, including the telegraf configuration file

The `marcell_drift_detection` folder contains the following folders and files:
- `static_data_handlers`: contains the code for the static part of the project, 
like batch train data loading and preprocessing and static model training, spark is used for this
- `data_streamers`: contains the classes that load the csv files and stream them with Kafka producers 
to simulate a real data stream
- `stream_preprocessors`: contains the code for the vanilla (non-flink) preprocessing of the data stream, 
these are used for preparing the data for the classifier models and drift detection methods
- `drift_detectors`: contains the classes for the drift detection methods there are multiple algorithms implemented
- `models`: contains the saved pre-trained models, 
these are created by the static data handlers (spark) and used by in the real-time stream mining pipeline
- `old`: contains the legacy notebooks and scripts that were used for testing and development, nothing important
- `results`: contains the notebooks for the evaluation of the drift detection methods and the results of the evaluation
- `pyflink`: contains the pyflink dependencies and the pyflink jobs for stream preprocessing and drift detection
- `static_model_trainer.ipynb`: spark notebook for loading, preprocessing and training the static models
- `data_streamer.ipynb`: spark notebook for streaming the csv data to kafka
- `stream_preprocessor.ipynb`: notebook for preprocessing the data stream
- `change_detector.ipynb`: notebook for running the drift detection methods
- `change_detector_multi_model.ipynb`: notebook for running the multi model drift detection method
