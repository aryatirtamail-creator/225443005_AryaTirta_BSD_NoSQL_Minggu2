import paho.mqtt.client as mqtt
import json
from pymongo import MongoClient
from datetime import datetime

mongo_client = MongoClient("mongodb://localhost:27017")
db = mongo_client["latihan_mqtt"]
collection = db["produksi_mqtt"]

broker = "broker.hivemq.com"
topic = "pabrik/produksi"

def on_connect(client, userdata, flags, rc):
    print("Terhubung ke broker")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode())

    data["timestamp"] = datetime.now()

    reject_rate = (data["reject"] / data["jumlah"]) * 100
    data["reject_rate"] = reject_rate

    if reject_rate > 5:
        print("⚠️ PERINGATAN! Reject rate terdeteksi tinggi:", reject_rate)
        data["peringatan"] = True
    else:
        data["peringatan"] = False

    collection.insert_one(data)

    print("Data masuk:", data)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, 1883, 60)
client.loop_forever()
