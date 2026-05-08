import paho.mqtt.client as mqtt
import json
import time
import random

broker = "broker.hivemq.com"
topic = "pabrik/produksi"

client = mqtt.Client()
client.connect(broker, 1883, 60)

mesin_list = ["CNC-01", "CNC-02", "CNC-03", "CNC-04"]
batch_list = ["B001", "B002", "B003", "B004"]

while True:
    data = {
        "batch": random.choice(batch_list),
        "mesin": random.choice(mesin_list),
        "jumlah": random.randint(100, 500),
        "reject": random.randint(0, 50)
    }

    client.publish(topic, json.dumps(data))
    print("Kirim:", data)

    time.sleep(3)
