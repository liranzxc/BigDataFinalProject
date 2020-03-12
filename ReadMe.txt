

for started a spark cluster first you need to download :

- docker
- docker-compose

in the root project we have docker-compose
you must be in "CMD" or terminal on the directory that contains docker-compose

# execute command : docker-compose up -d

please wait  , cluster spark will be created  ( master + 1 worker)

on the project have spark_example folder that contains a test script . please run him before started .

the script connected to spark and execute a "ADD" operation .

please note need to pip install all packages .

have fun :)

** for close docker need to go directory and execute : docker-compose down

Running Ubuntu requires Java 8 version.

## example run :

(base) lirannh@192:~/Desktop/BigData$ docker-compose up -d
WARNING: The Docker Engine you're using is running in swarm mode.

Compose does not use swarm mode to deploy services to multiple nodes in a swarm. All containers will be scheduled on the current node.

To deploy your application across the swarm, use `docker stack deploy`.

Creating network "bigdata_default" with the default driver
Creating spark-master ... done
Creating spark-worker-1 ... done
(base) lirannh@192:~/Desktop/BigData$
(base) lirannh@192:~/Desktop/BigData$
(base) lirannh@192:~/Desktop/BigData$ python spark_example/sparkHelloWorld.py
20/02/22 17:47:55 WARN NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable
Using Spark's default log4j profile: org/apache/spark/log4j-defaults.properties
Setting default log level to "WARN".
To adjust logging level use sc.setLogLevel(newLevel). For SparkR, use setLogLevel(newLevel).
10
(base) lirannh@192:~/Desktop/BigData$


## docker-compose down

(base) lirannh@192:~/Desktop/BigData$ docker-compose down
Stopping spark-worker-1 ... done
Stopping spark-master   ... done
Removing spark-worker-1 ... done
Removing spark-master   ... done
Removing network bigdata_default
(base) lirannh@192:~/Desktop/BigData$
