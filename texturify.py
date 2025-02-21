import cv2
import numpy as np
import os
from PIL import Image

def tile_texture(texture, width, height):
    """Tile a texture image to cover a given width and height."""
    tiled_texture = np.tile(texture, (height // texture.shape[0] + 1, width // texture.shape[1] + 1, 1))
    return tiled_texture[:height, :width]

def apply_texture_to_white(content_path, texture_path, output_path, texture_size):
    """Apply a tiled texture to white areas of an image, leaving black and transparent areas untouched."""
    # Load images
    content = cv2.imread(content_path, cv2.IMREAD_UNCHANGED)
    texture = cv2.imread(texture_path, cv2.IMREAD_UNCHANGED)

    if content is None:
        raise FileNotFoundError(f"Content image not found at {content_path}")
    if texture is None:
        raise FileNotFoundError(f"Texture image not found at {texture_path}")

    # Extract alpha channel and RGB channels
    if content.shape[2] == 4:
        alpha = content[:, :, 3] / 255.0
        content_rgb = content[:, :, :3] / 255.0
    else:
        alpha = np.ones((content.shape[0], content.shape[1]), dtype=np.float32)
        content_rgb = content[:, :, :3] / 255.0

    # Mask for white areas: RGB close to white and alpha > 0
    white_mask = np.all(content_rgb >= 0.75, axis=-1) & (alpha > 0)

    # Mask for black areas: RGB close to black and alpha > 0
    black_mask = np.all(content_rgb <= 0.25, axis=-1) & (alpha > 0)

    # Resize texture
    texture = cv2.resize(texture, (texture_size, texture_size), interpolation=cv2.INTER_NEAREST).astype(np.float32) / 255.0

    if texture.shape[-1] == 4:
        texture = texture[:, :, :3]  # Drop the alpha channel

    # Tile the texture
    tiled_texture = tile_texture(texture, content.shape[1], content.shape[0])

    # Initialize result with black areas preserved
    result = np.zeros_like(content_rgb, dtype=np.float32)
    result[black_mask] = [0, 0, 0]  # Keep black areas black

    # Apply texture to white areas
    result[white_mask] = tiled_texture[white_mask]

    # Keep non-white, non-black areas as original
    other_mask = ~(white_mask | black_mask)
    result[other_mask] = content_rgb[other_mask]

    # Combine with original alpha
    result = (result * 255).astype(np.uint8)
    result_with_alpha = np.dstack((result, (alpha[:, :, np.newaxis] * 255).astype(np.uint8)))


    # Save the result
    success = cv2.imwrite(output_path, result_with_alpha)
    if not success:
        raise FileNotFoundError(f"Failed to write the image to {output_path}")
    print("Image saved successfully!")


if __name__ == "__main__":
    try:
        content_path = "content.png"
        texture_path = "texture.png"
        output_path = "textured_output.png"
        apply_texture_to_white(content_path, texture_path, output_path, texture_size=250)
    except Exception as e:
        print(f"Error: {e}")
