from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import subprocess
import os
import base64
import shutil

app = Flask(__name__)

# Enable CORS for all domains (adjust if you need to restrict to specific origins)
CORS(app, resources={r"/stylize": {"origins": "http://localhost:5173"}})

@app.route('/stylize', methods=['POST'])
def stylize():
    try:
        # Get the content image as a base64 string and style name from the request
        content_base64 = request.form.get('content')  # The base64 content image
        style_name = request.form.get('style_name')   # The style name

        if not content_base64 or not style_name:
            return jsonify({'error': 'Content image in base64 and style name are required'}), 400

        # Decode the base64 string to save as an image file
        content_image_path = '/app/content.jpg'
        with open(content_image_path, 'wb') as img_file:
            img_file.write(base64.b64decode(content_base64))

        # Map the style name to the corresponding style image
        style_map = {
            'pencil': '/app/pencil.jpg',
            'monet': '/app/monet.jpg',
            'comic': '/app/comic.jpg'
        }

        # Check if the style_name is valid
        if style_name not in style_map:
            return jsonify({'error': 'Invalid style name. Choose from: pencil, monet, comic'}), 400

        # Copy the selected style image to /app/style.jpg
        style_image_path = style_map[style_name]
        shutil.copy(style_image_path, '/app/style.jpg')

        # Call the stylize.py script
        result = subprocess.run(['python', '/app/stylize.py'], capture_output=True, text=True)

        if result.returncode != 0:
            return jsonify({'error': 'Error running stylize.py', 'message': result.stderr}), 500

        # Assuming the script generates the stylized image at '/app/stylized_output.png'
        output_path = '/app/stylized_output.png'

        # Check if the output file was created
        if not os.path.exists(output_path):
            return jsonify({'error': 'Stylized output file not found'}), 500

        # Open the generated image and convert it to base64
        with open(output_path, 'rb') as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode('utf-8')

        # Return the base64 string in the response
        return jsonify({'output': img_base64})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
