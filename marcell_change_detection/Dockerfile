FROM apache/flink:1.14.0

#COPY ./stream_miner.py /opt/pyflink_app/pyflink_stream_miner.py
RUN ls -la

WORKDIR /opt/pyflink_app

ENTRYPOINT ["python", "pyflink_stream_miner.py"]
