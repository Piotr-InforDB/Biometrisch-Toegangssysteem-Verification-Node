from time import sleep
import platform
import cv2
import paho.mqtt.client as mqtt

from messageHandler import MessageHandler

MQTT_USERNAME = 'verification_node'
MQTT_PASSWORD = 'admin'
MQTT_BROKER = 'accesscontrol.home'
# MQTT_BROKER = 'localhost'
MQTT_PORT = 1883
MQTT_TOPICS = [
    'presence',
    'client/identity',
]

FPS = 30
last_frame = None
messageHandler = MessageHandler()

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")
    messageHandler.set_client(client)
    for topic in MQTT_TOPICS:
        client.subscribe(topic)

def on_message(client, userdata, msg):
    messageHandler.handle_message(msg.topic, msg.payload.decode())


client = mqtt.Client(client_id=MQTT_USERNAME)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)

if platform.system() == 'Windows':
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)
else:
    from picamera2 import Picamera2

    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (300, 300)})
    picam2.configure(config)
    picam2.start()

client.loop_start()

while True:
    if platform.system() == 'Windows':
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            continue
    else:
        frame = picam2.capture_array()

    ret, jpeg = cv2.imencode('.jpg', frame)

    if ret:
        client.publish("webcam/feed", jpeg.tobytes())

    sleep(1 / FPS)