# A jelenlegi szituáció és prlemák a flinkkel kapcsolatban

## Setup
`stream_miner.py` egy flink job, ami a `hai-preprocessed` topicból olvas be, és a `hai-results` topicba írja a feldolgozott adatokat.
A flink egy docker containerben fut, a többi szükséges komponenssel együtt. Ezek a `pipeline` mappában vannak egy docker-compose fileban.
There is a Dockerfile in the `marcell_change_detection` folder that builds the docker image for the flink job, but it is currently not used.
Van egy Dockerfile a 'marcell_change_detection' mappában, ami a flink jobhoz készít egy docker image-et, de jelenleg nem használom, mert nem ment.
I tried many variations of the docker-compose file, including the definition of the flink job in the docker-compose file, but none of them worked.
Prábáltam többféle docker-compose file-t, volt olyan, ahol a docker-compose-ban vettem fel egy új pyflink job-ot, de egyik sem működött.

## Problémák
A legfőbb probléma, hogy az interneten nem találok egy egységes leírást arról, 
hogy hogyan kell a a pyflinket használni, minenhol mást írnak, valamint a flinket dockerben futtatni. 
Ezért minden megoldással foglalkoztam már, sikertelenül.

## Amit eddig kiderítettem:
 - kell egy flink-connector-kafka jar file a flinknek, ez megvan.
 - ha flink environmentet hozok létre, akkor kell python telepítés, hogy a flink tudja futtatni a python scriptet.


## Hasznos linkek
- https://wicaksonodiaz.medium.com/setup-pyflink-development-environment-76d8491a9ad7
- https://medium.com/@sant1/flink-docker-kafka-faee9c0f1580
- https://github.com/qooba/flink-with-ai/blob/main/docker/flink/Dockerfile

