from kafka import KafkaProducer
import json


class Producer:
    def __init__(self, kafkaServer, topicSend):
        self.topicSend = topicSend
        self.producer = KafkaProducer(bootstrap_servers=[kafkaServer],value_serializer=lambda m: json.dumps(m).encode('ascii'))

    def send(self, message):
        ack = self.producer.send(self.topicSend, message)
        return ack
