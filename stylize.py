# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import numpy as np
import base64
import io
import PIL.Image
import tensorflow_hub as hub
import sys
import json

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

# Function to decode base64 string to image tensor
def base64_to_tensor(base64_str):
    print("Decoding base64 string to image tensor...")
    img_data = base64.b64decode(base64_str)
    img = PIL.Image.open(io.BytesIO(img_data)).convert("RGB")

    # Preprocess image for model
    max_dim = 512
    img = np.array(img) / 255.0  # Normalize
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    scale = max_dim / max(shape)
    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    print(f"Image shape after resizing: {img.shape}")
    return img

# Function to encode tensor to base64
def tensor_to_base64(tensor):
    print("Converting tensor to base64 string...")
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    
    img = PIL.Image.fromarray(tensor)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    encoded = base64.b64encode(buffered.getvalue()).decode("utf-8")
    print(f"Base64 string length: {len(encoded)} characters")
    return encoded

def main():
    print("Starting the main process...")

    # Read base64 JSON input from command line
    input_json = json.loads(sys.argv[1])
    content_b64 = input_json['content']
    style_b64 = input_json['style']

    print(f"Received base64 content and style strings. Content length: {len(content_b64)}, Style length: {len(style_b64)}")

    # Convert base64 to tensors
    content_image = base64_to_tensor(content_b64)
    style_image = base64_to_tensor(style_b64)

    print("Base64 strings decoded to tensors.")

    # Load the style transfer model
    print("Loading the style transfer model...")
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    print("Model loaded successfully.")

    # Perform style transfer
    print("Performing style transfer...")
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    print("Style transfer completed.")

    # Convert stylized image to base64
    print("Converting stylized image to base64...")
    result_b64 = tensor_to_base64(stylized_image)

    # Print output as JSON
    print("Returning the final stylized image as base64 encoded JSON...")
    print(json.dumps({"stylized_image": result_b64}))

if __name__ == "__main__":
    main()
