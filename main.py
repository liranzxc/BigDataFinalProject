from producer.producer import Producer
from worker.consumer import Consumer

message = {"liran": 123}

kafkaServer = "localhost:9092"
topicSend = "send"
prod = Producer(kafkaServer, topicSend)
consumer = Consumer(kafkaServer, topicSend)

prod.send(message)


consumer.startReceive(lambda m: m)
