FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    libcamera0 \
    libcamera-dev \
    python3-libcamera \
    python3-picamera2 \
    && pip install --upgrade pip \
    && pip install paho-mqtt picamera2 opencv-python \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

CMD ["python", "picamera.py"]