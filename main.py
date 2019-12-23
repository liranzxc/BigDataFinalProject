from producer import Producer
from worker import Consumer

message = {"liran": 123}

kafkaServer = ""
topicSend = "send"
topicReceive = "send"
prod = Producer(kafkaServer, topicSend)

prod.send(message)

consumer = Consumer(kafkaServer, topicReceive)

consumer.startReceive(lambda m: m)
