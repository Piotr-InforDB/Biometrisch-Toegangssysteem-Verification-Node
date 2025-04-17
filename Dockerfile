FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libcamera0 \
    libcamera-dev \
    python3-libcamera \
    python3-picamera2 \
    python3-opencv \
    libopencv-dev \
    && pip install --upgrade pip \
    && pip install --no-cache-dir \
        paho-mqtt \
        picamera2 \
        opencv-python-headless \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "picamera.py"]