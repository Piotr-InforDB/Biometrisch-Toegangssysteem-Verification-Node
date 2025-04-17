FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libcamera0.0.3 \
    libcamera-dev \
    gstreamer1.0-libcamera \
    && pip install --upgrade pip \
    && pip install --no-cache-dir \
        paho-mqtt \
        picamera2 \
        opencv-python-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "picamera.py"]