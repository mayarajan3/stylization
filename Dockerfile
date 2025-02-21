# Use an official Python base image (compatible with ARM64)
FROM --platform=linux/amd64 python:3.8

# Set environment variable to prevent Python output buffering
ENV PYTHONUNBUFFERED=1

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python

# Set working directory inside the container
RUN mkdir -p /app && chmod 777 /app

# Set working directory inside the container
WORKDIR /app

# Verify that /app exists
RUN ls -l /app

RUN apt-get update && apt-get install -y libgl1

# Copy the Python script into the container
COPY stylize.py /app/stylize.py
COPY texturify.py /app/texturify.py

COPY fuzzy.png /app/fuzzy.png
COPY fuzzy.png /app/texture.png
COPY wave.jpg /app/content.png

COPY api_server.py /app/api_server.py

# Copy the TensorFlow .whl file into the container
# COPY tensorflow-2.3.0-cp38-cp38-linux_x86_64.whl /app/tensorflow-2.3.0-cp38-cp38-linux_x86_64.whl

# Install required Python packages
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir numpy && pip install protobuf==3.20.0 && pip install flask && pip install flask-cors && pip install opencv-python-headless && pip install pillow

EXPOSE 5000

# Ensure the script runs as expected
CMD ["python", "/app/api_server.py"]
