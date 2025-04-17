FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libcap-dev \
    libjpeg-dev \
    libtiff-dev \
    libpng-dev \
    libavcodec-dev \
    libavformat-dev \
    libswscale-dev \
    libv4l-dev \
    libxvidcore-dev \
    libx264-dev \
    libatlas-base-dev \
    libgl1-mesa-glx \
    git \
    && apt-get clean

RUN pip install --no-cache-dir \
    opencv-python-headless \
    paho-mqtt \
    picamera2

WORKDIR /app
COPY . .

CMD ["python", "main.py"]
