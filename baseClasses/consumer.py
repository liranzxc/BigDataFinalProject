from kafka import KafkaConsumer
import json


class Consumer:
    def __init__(self, kafkaServer, topicReceive):
        self.consumer = KafkaConsumer(
            topicReceive,
            bootstrap_servers=[kafkaServer],
            group_id='liran', api_version=(0, 11, 5))
        self.topicReceive = topicReceive

    def startReceive(self, methodMessages):
        print("start receive from topic '{}'".format(self.topicReceive))
        for message in self.consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            try:
                messageJson = message.value.decode('utf-8')
                messageJson = json.loads(messageJson)
                methodMessages(messageJson)
            except Exception as e:
                print(e)
                pass

            # print(messageJson)
            # print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
            #                                      message.offset, message.key,
            #                                      message.value))

