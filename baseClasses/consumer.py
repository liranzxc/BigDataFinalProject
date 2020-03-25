from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, kafka_server, topic_receive):
        self.consumer = KafkaConsumer(
            topic_receive,
            auto_offset_reset='earliest',
            bootstrap_servers=[kafka_server],
            sasl_plain_username="user", sasl_plain_password="bitnami",
            group_id=None)
        self.topic_receive = topic_receive

    def start_receive(self, method_messages,extraData=None):
        print("start receive from topic {}".format(self.topic_receive))
        for message in self.consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            try:
                message_json = message.value.decode('utf-8')
                message_json = json.loads(message_json)
                method_messages(message_json, extraData=extraData)
            except Exception as e:
                print(e)
                pass

            # print(message_json)
            # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            #                                      message.offset, message.key,
            #                                      message.value))

