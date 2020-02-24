from baseClasses.producer import Producer

kafkaServer = "172.25.0.12:9092"
topicToSend = "work"

pro = Producer(kafkaServer, topicToSend)
future = (pro.send({"artist": "liran nachmang"}))
result = future.get(timeout=60)
print(result)


