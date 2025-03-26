import cv2
import paho.mqtt.client as mqtt
import numpy as np
from tensorflow.python.data.experimental.ops.testing import sleep

MQTT_BROKER = 'accesscontrol.home'

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="verification_node")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="verification_node", password="admin")
client.connect(MQTT_BROKER, 1883)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Failed to grab frame.")
        break

    success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 50])

    if success:
        client.publish("webcam/feed", buffer.tobytes())
    else:
        print("Failed to encode frame.")

    client.loop()
