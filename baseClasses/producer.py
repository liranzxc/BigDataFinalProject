from bson import json_util
from kafka import KafkaProducer
import json


class Producer:
    def __init__(self, kafka_server, topic_send):
        self.topicSend = topic_send
        self.producer = KafkaProducer(bootstrap_servers=[kafka_server])
        # value_serializer=lambda x: dumps(x).encode('utf-8')))

    def send(self, message):
        ack = self.producer.send(self.topicSend, json.dumps(message, default=json_util.default).encode('utf-8')) \
            .add_callback(self.on_send_success) \
            .add_errback(self.on_send_error)
        return ack

    def on_send_success(self, record_metadata):
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def on_send_error(self, excp):
        print('I am an errback', exc_info=excp)
        # handle exception
