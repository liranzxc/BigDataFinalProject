import json

from kafka import KafkaConsumer


class Consumer:
    def __init__(self, kafka_server, topic_receive):
        self.consumer = KafkaConsumer(
            topic_receive,
            auto_offset_reset='earliest',
            bootstrap_servers=[kafka_server],
            sasl_plain_username="user", sasl_plain_password="bitnami",
            group_id=None)
        self.topic_receive = topic_receive

    def start_receive(self, method_messages, extra_data=None):
        print("start receive from topic {}".format(self.topic_receive))
        for message in self.consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            try:
                message_json = message.value.decode('utf-8')
                message_json = json.loads(message_json)
                method_messages(message_json, extra_data=extra_data)
            except Exception as e:
                print(e)
                pass