# A jelenlegi szituáció és prlemák a flinkkel kapcsolatban

# Update:
A flink maga megy, jelenleg kicsit csúnyán betettem a docker compose-t és a Dockerfile-t is a 
`marcell_change_detection` mappába, hogy ne legyen gond az elérési utakkal.
A flink megy, elvileg meg is van adva neki ez a folder, ahol vannak a scriptek, de automatikusan nem fedezi fel őket.
Ezért a flink UI-ban és a dockerbe belépve a flink CLI-ban próbáltam futtatni a jobot, de azt mondja, hogy csak JAR fájlokat tud futtatni.
Aminek elvileg nem így kellene lennije.
Túl nagy fájlok, ezért nem tudtam feltenni githubra, a marcell_change_detection mappába kell tenni őket.
- https://files.pythonhosted.org/packages/ad/ef/f89e77d4edf273992b172ceb382e0da97aa6b156f6d232ed0bb0bbb0fa1f/apache-flink-1.18.0.tar.gz
- https://files.pythonhosted.org/packages/af/41/63f7cebe2c450dcc6ae8d12e916b2765b4600e4ac18253bb8a6d27235938/apache-flink-libraries-1.18.0.tar.gz

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

