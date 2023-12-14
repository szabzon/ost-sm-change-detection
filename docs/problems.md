# A jelenlegi szituáció és prlemák a flinkkel kapcsolatban


# Update 2:
- Kicsit javítottam a kód minőségén és a mappa struktúrán, hogy kezelhetőbb legyen a projekt.
- Még továbbra is minden a `marcell_change_detection` mappában van, ezen belül dolgozok.
- Ez alól egy kivétel van, a `data_loading/data_loader.ipynb` fájl, ami a test data streameléséhez kell.
- A compose-ban és Dockerfile-ban található elérési utak módosultak kicsit.
- A flink dependency-ket betettem a `flink_dependencies` mappába.
- A `drift_detectors` mappában vannak továbbra is a drift detektáló algoritmusok, ezeket bővítettem.
- A `data_loaders` mappában vannak a data loader-ek, mind a training data-hoz és mind a stream-hez (test data) ezeket is refaktoráltam részben.
- A `model_handlers` mappában van a model trainer-tester osztály.
- A `stream_miner.ipynb` fájlban található a jelenleg is futtatható drift detekció FLINK NÉLKÜL.
- A `stream_miner.py` fájlban található a jelenleg még nem futtatható drift detekció FLINK JOB. Ezt kéne valahogy futtatni, de nem megy.
- A `stream_preprocessor.ipynb` fájlban található a stream preprocessor, ami a stream-et előkészíti a drift detekcióhoz. Később ezt is ki szeretném szervezni Flink job-ba.

**A jelenlegiek futtatása:**
1. Getting started részben leírtak szerint kell elindítani a docker-compose file-t, annyi különbséggel, hogy a a `marcell_change_detection` mappában kell lenni, így a compose file-t is onnan kell elindítani.
2. A `../data_loading/data_loader.ipynb` fájlt futtatva lehet streamelni a test adatokat a `hai-input` kafka topicba.
3. A `stream_preprocessor.ipynb` fájlt futtatva lehet előkészíteni a stream-et a drift detekcióhoz. Ez a `hai-input` topicból olvas be, és a `hai-preprocessed` topicba írja a feldolgozott adatokat.
4. A `stream_miner.ipynb` fájlt futtatva lehet futtatni a drift detekciót FLINK NÉLKÜL. Ez a `hai-preprocessed` topicból olvas be, és a `hai-results` topicba írja a feldolgozott adatokat.
5. A `stream_miner.py`-ban található flink job-ot kéne futtatni a 4. pont helyett, ha menne. Elvileg a különbség csak a flink-használatában van, a többi ugyanaz, mint az ipynb. (Ehhez fontos, hogy az előző update-ben megadott linkeken lévő fájlokat be kell másolni a `flink_dependencies` mappába.) Továbbá, a `docker build --tag pyflink:1.14.0 . ` parancsot ki kell adni a `marcell_change_detection` mappában, hogy legyen egy docker image, amit a compose file használhat.

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

