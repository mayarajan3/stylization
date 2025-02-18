# Use an official Python base image (compatible with ARM64)
FROM --platform=linux/amd64 python:3.8

# Set environment variable to prevent Python output buffering
ENV PYTHONUNBUFFERED=1

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set working directory inside the container
RUN mkdir -p /app

# Set working directory inside the container
WORKDIR /app

# Verify that /app exists
RUN ls -l /app

# Copy the Python script into the container
COPY stylize.py /app/stylize.py

COPY content.jpg /app/content.jpg
COPY style.jpg /app/style.jpg

# Copy the TensorFlow .whl file into the container
# CCOPY tensorflow-2.3.0-cp38-cp38-linux_x86_64.whl /app/tensorflow-2.3.0-cp38-cp38-linux_x86_64.whl

# Install required Python packages
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir tensorflow-hub pillow numpy && \
    pip install "https://drive.google.com/uc?export=download&id=1T1wJsyZopeNUqCnqjeRbCImxE_BhDlDN" && pip install protobuf==3.20.0

# Ensure the script runs as expected
CMD ["python", "/app/stylize.py"]
