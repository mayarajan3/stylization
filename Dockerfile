FROM tensorflow/tensorflow:2.11.0 AS base

# Check if the base image is compatible with ARM64
RUN uname -m

# Set the correct platform
FROM --platform=linux/arm64 base

# Set environment variable to prevent Python output buffering
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy the Python script into the container
COPY stylize.py /app/stylize.py

# Install required Python packages
RUN python3 -m pip install --upgrade pip && \
    pip install --no-cache-dir tensorflow-hub pillow numpy

# Ensure the script runs as expected
CMD ["python", "/app/stylize.py"]
