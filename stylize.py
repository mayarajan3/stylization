# -*- coding: utf-8 -*-
import os
import tensorflow as tf
import numpy as np
import io
import PIL.Image
import tensorflow_hub as hub
import json

# Load compressed models from tensorflow_hub
os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

def load_image(image_path):
    print(f"Loading image from {image_path}...")
    img = PIL.Image.open(image_path).convert("RGB")
    
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

def tensor_to_image(tensor, output_path="stylized_output.png"):
    print("Saving stylized image...")
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    
    img = PIL.Image.fromarray(tensor)
    img.save(output_path)
    print(f"Stylized image saved to {output_path}")

def main():
    print("Starting the style transfer process...")
    
    # Define image paths
    content_path = "content.jpg"
    style_path = "style.jpg"
    
    if not os.path.exists(content_path) or not os.path.exists(style_path):
        print("Error: Ensure both 'content.jpg' and 'style.jpg' exist in the script directory.")
        return
    
    # Load images
    content_image = load_image(content_path)
    style_image = load_image(style_path)
    
    # Load the style transfer model
    print("Loading the style transfer model...")
    hub_model = hub.load('https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2')
    print("Model loaded successfully.")
    
    # Perform style transfer
    print("Performing style transfer...")
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    print("Style transfer completed.")
    
    # Save stylized image
    tensor_to_image(stylized_image)

if __name__ == "__main__":
    main()
