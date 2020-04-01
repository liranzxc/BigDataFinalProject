from bson import json_util
from kafka import KafkaProducer
import json


class Producer:
    def __init__(self, kafka_server, topic_send):
        self.topic = topic_send
        self.producer = KafkaProducer(bootstrap_servers=[kafka_server], sasl_plain_username="user", sasl_plain_password="bitnami")

    def send(self, message):
        ack = self.producer.send(self.topic, json.dumps(message, default=json_util.default).encode('utf-8')) \
            .add_callback(self.on_send_success) \
            .add_errback(self.on_send_error)
        return ack

    def on_send_success(self, record_metadata):
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def on_send_error(self, exception):
        print('Error: {}'.format(exception))
        # handle exception
        # TODO ?
