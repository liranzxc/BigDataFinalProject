Make sure Docker is up with linux containers before pressing on start.bat

Install Docker and operate with linux containers
    - Build all containers
        1. open cmd inside big-data-servers
        2. $docker-compose up -d (servers should build and go up)
        3. $docker-compose -f docker-compose-producer.yml build
        4. $docker-compose -f docker-compose-consumer.yml build
    - Start Client API
        1. $python controller-server.py (server api for client - localhost:5000)
    - Start client
        1. Install npm (https://nodejs.org/en/ - version 12.16)
        2. cd into song-viewer folder
        3. $npm install -g @angular/cli
        4. $npm install
        5. $ng serve (server should be open at localhost:4200)

To start a spark cluster, you need to download :

- docker 1.25.0
- docker-compose 1.25.0

in the root project we have docker-compose
you must be in "CMD" or terminal on the directory that contains docker-compose

# execute command : docker-compose up -d

please wait,a spark cluster will be created  (master + 1 worker)

on the project have spark_example folder that contains a test script. please run him before beginning to see if spark works.

The script is connected to spark and executes an "ADD" operation.

please note need to pip install all packages in requirements

in the python console write
nltk.download('wordnet')

run in the folder context
docker build -t {image-name} .
make sure docker-compose for producer/consumer use the same image-name you built with.

have fun :)

** for close docker need to go directory and execute : docker-compose down

Running Ubuntu requires Java 8 version.


## docker-compose down

$ docker-compose down

# scale

docker-compose up -d --scale spark-worker=2
docker-compose --file docker-compose-producer.yml up