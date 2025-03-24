import cv2
import paho.mqtt.client as mqtt
import numpy as np

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="verification_node")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="verification_node", password="admin")
client.connect("accesscontrol.home", 1883)

width, height = 640, 480

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'YUYV'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

if not cap.isOpened():
    print("Camera failed to open!")
    exit()

client.loop_start()

while True:
    ret, frame = cap.read()
    if not ret or frame is None:
        print("Failed to grab frame.")
        continue

    # Fix the shape explicitly here:
    if frame.shape[0] == 1 or len(frame.shape) == 2:
        frame = frame.reshape((height, width, 2))

    # Now safely convert YUYV to BGR
    frame_bgr = cv2.cvtColor(frame, cv2.COLOR_YUV2BGR_YUYV)

    success, buffer = cv2.imencode('.jpg', frame_bgr, [cv2.IMWRITE_JPEG_QUALITY, 50])

    if success:
        client.publish("webcam/feed", buffer.tobytes())
    else:
        print("Failed to encode frame.")
