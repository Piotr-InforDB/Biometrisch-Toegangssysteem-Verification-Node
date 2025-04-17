FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    libopencv-dev \
    libcamera-dev \
    libcamera-apps \
    libatlas-base-dev \
    python3-opencv \
    ffmpeg \
    libjpeg-dev \
    libpng-dev \
    libtiff-dev \
    libx264-dev \
    git \
    && apt-get clean

RUN pip install --no-cache-dir \
    paho-mqtt \
    opencv-python-headless \
    picamera2

WORKDIR /app

COPY script.py .

CMD ["python", "picamera.py"]
