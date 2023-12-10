#!/bin/bash

influx setup \
  --bucket $INFLUXDB_BUCKET \
  --retention 30d \
  --token admin \
  --org $INFLUXDB_ORG \
  --username $INFLUXDB_ADMIN_USER \
  --password $INFLUXDB_ADMIN_PASSWORD \
  --host=$INFLUXDB_HOST \
  --force