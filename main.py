from producer.producer import Producer
from worker.consumer import Consumer

message = {"liran": 200}

kafkaServer = "localhost:9092"
topicSend = "send"  # or receive
prod = Producer(kafkaServer, topicSend)
consumer = Consumer(kafkaServer, topicSend)

for i in range(2):
    prod.send({"liran": i})


consumer.startReceive(lambda m: print(m))
