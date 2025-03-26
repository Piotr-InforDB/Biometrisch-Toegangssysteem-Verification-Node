from picamera2 import Picamera2
import cv2
import paho.mqtt.client as mqtt

# MQTT setup
def on_connect(client, userdata, flags, rc, properties=None):
    print(f"Connected with result code: {rc}")

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

client = mqtt.Client(client_id="verification_node")
client.on_connect = on_connect
client.on_message = on_message

client.username_pw_set(username="verification_node", password="admin")
client.connect("accesscontrol.home", 1883)

# PiCamera2 setup
picam2 = Picamera2()
config = picam2.create_video_configuration(main={"format": 'XRGB8888', "size": (480, 360)})
picam2.configure(config)
picam2.start()

client.loop_start()

while True:
    frame = picam2.capture_array()
    ret, jpeg = cv2.imencode('.jpg', frame)

    if ret:
        client.publish("webcam/feed", jpeg.tobytes())