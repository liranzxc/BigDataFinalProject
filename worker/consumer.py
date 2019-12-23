from kafka import KafkaConsumer


class Consumer:
    def __init__(self, kafkaServer, topicReceive):
        self.consumer = KafkaConsumer(topicReceive, bootstrap_servers=[kafkaServer])

    def startReceive(self, methodMessages):
        for message in self.consumer:
            # message value and key are raw bytes -- decode if necessary!
            # e.g., for unicode: `message.value.decode('utf-8')`
            print("%s:%d:%d: key=%s value=%s" % (message.topic, message.partition,
                                                 message.offset, message.key,
                                                 message.value))

            methodMessages(message)
