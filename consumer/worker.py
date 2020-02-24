from baseClasses.consumer import Consumer
from models.song import Song
import json

def SongWork(song:Song):
    print("starting work on song ",song)
    print(song["artist"])
    print("here")




if __name__ == "__main__":
    kafkaServer = "172.25.0.12:9092"
    topicReceive = "work"
    worker = Consumer(kafkaServer, topicReceive)

    worker.startReceive(SongWork)
    print("here")
