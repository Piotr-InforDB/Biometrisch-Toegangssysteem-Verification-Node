FROM arm64v8/python:3.11-slim-bullseye

WORKDIR /app

RUN echo "deb http://archive.raspberrypi.org/debian/ bullseye main" >> /etc/apt/sources.list.d/raspi.list && \
    apt-get update && \
    apt-get install -y wget && \
    wget -O - https://archive.raspberrypi.org/debian/raspberrypi.gpg.key | apt-key add - && \
    apt-get update && \
    apt-get install -y \
    gcc \
    python3-dev \
    libcap-dev \
    python3-libcamera \
    python3-picamera2 \
    libcamera0 \
    libcamera-dev \
    gstreamer1.0-libcamera \
    && pip install --upgrade pip \
    && pip install --no-cache-dir \
        paho-mqtt \
        opencv-python-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "picamera.py"]