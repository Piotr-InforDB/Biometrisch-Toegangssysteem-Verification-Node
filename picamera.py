from picamera2 import Picamera2
import cv2
import paho.mqtt.client as mqtt

MQTT_USERNAME = 'verification_node'
MQTT_PASSWORD = 'admin'
MQTT_BROKER = 'accesscontrol.home'
MQTT_PORT = 1883

# MQTT setup
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(client_id=MQTT_USERNAME)
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username=MQTT_USERNAME, password=MQTT_PASSWORD)
client.connect(MQTT_BROKER, MQTT_PORT)

# PiCamera2 setup
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (300, 300)})
picam2.configure(config)
picam2.start()

client.loop_start()

while True:
    frame = picam2.capture_array()
    ret, jpeg = cv2.imencode('.jpg', frame)

    if ret:
        client.publish("webcam/feed", jpeg.tobytes())