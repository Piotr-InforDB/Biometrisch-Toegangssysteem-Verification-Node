FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install paho-mqtt picamera2 opencv-python

COPY . .

CMD ["python", "picamera.py"]