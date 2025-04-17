FROM python:3.11-slim-bullseye

# System dependencies for OpenCV + picamera2
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
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

# Install Python dependencies
RUN pip install --no-cache-dir \
    opencv-python-headless \
    paho-mqtt \
    picamera2

# Add your script
WORKDIR /app
COPY . .

CMD ["python", "picamera.py"]
