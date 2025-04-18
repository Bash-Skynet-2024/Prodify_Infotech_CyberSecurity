from flask import Flask, render_template_string, request, send_file, flash, redirect, url_for, make_response
from PIL import Image
import random
import os
import io
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# HTML template as a string
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Encryption/Decryption Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f5f5f5;
        }
        .container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        h1 {
            color: #333;
            text-align: center;
            margin-bottom: 30px;
        }
        .form-group {
            margin-bottom: 20px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #555;
        }
        input[type="file"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            background-color: #fff;
        }
        .operation-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 20px;
        }
        button {
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
            transition: background-color 0.3s;
        }
        .encrypt-btn {
            background-color: #4CAF50;
            color: white;
        }
        .decrypt-btn {
            background-color: #2196F3;
            color: white;
        }
        button:hover {
            opacity: 0.9;
        }
        .flash-messages {
            margin-bottom: 20px;
        }
        .flash-message {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
            background-color: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        .flash-message.success {
            background-color: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Encryption/Decryption Tool</h1>
        
        {% with messages = get_flashed_messages() %}
            {% if messages %}
                <div class="flash-messages">
                    {% for message in messages %}
                        <div class="flash-message {% if 'success' in message.lower() %}success{% endif %}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}

        <form action="{{ url_for('process_image') }}" method="post" enctype="multipart/form-data">
            <div class="form-group">
                <label for="file">Select Image File:</label>
                <input type="file" id="file" name="file" accept=".png,.jpg,.jpeg,.gif" required>
            </div>
            
            <div class="operation-buttons">
                <button type="submit" name="operation" value="encrypt" class="encrypt-btn">Encrypt Image</button>
                <button type="submit" name="operation" value="decrypt" class="decrypt-btn">Decrypt Image</button>
            </div>
        </form>
    </div>
</body>
</html>
'''

# Define constants for encryption
KEY = 123  # Random key for XOR operation
RANDOM_SEED = 42  # Used for deterministic shuffling
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def xor_pixel(pixel, key):
    """Perform XOR operation on the RGB values of a pixel."""
    return (
        pixel[0] ^ key,
        pixel[1] ^ key,
        pixel[2] ^ key
    )

def process_image_data(img, operation='encrypt'):
    """Process image data for either encryption or decryption."""
    pixels = img.load()
    width, height = img.size
    
    # Set random seed for consistent shuffling
    random.seed(RANDOM_SEED)
    
    # Create list of all pixel positions
    positions = [(i, j) for i in range(width) for j in range(height)]
    
    if operation == 'encrypt':
        # For encryption, shuffle the positions
        random.shuffle(positions)
    else:
        # For decryption, reverse the shuffle by sorting
        positions.sort(key=lambda pos: random.random())
        positions.reverse()
    
    # Create new image for processed data
    processed_img = Image.new('RGB', (width, height))
    processed_pixels = processed_img.load()
    
    # Process each pixel
    for idx, (i, j) in enumerate(positions):
        pixel = pixels[i, j]
        processed_pixel = xor_pixel(pixel, KEY)
        
        if operation == 'encrypt':
            new_i, new_j = positions[idx]
        else:
            new_i, new_j = i, j
            
        processed_pixels[new_i, new_j] = processed_pixel
    
    return processed_img

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        flash('No file selected')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected')
        return redirect(url_for('index'))

    if not allowed_file(file.filename):
        flash('Invalid file type')
        return redirect(url_for('index'))

    operation = request.form.get('operation')
    if operation not in ['encrypt', 'decrypt']:
        flash('Invalid operation')
        return redirect(url_for('index'))

    try:
        # Read the input image
        img = Image.open(file.stream)
        
        # Process the image
        processed_img = process_image_data(img, operation)
        
        # Save to bytes buffer
        img_io = io.BytesIO()
        processed_img.save(img_io, 'PNG')
        img_io.seek(0)
        
        # Create response
        response = make_response(send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name=f"{operation}ed_{secure_filename(file.filename)}"
        ))
        
        flash(f'Image {operation}ed successfully!')
        return response

    except Exception as e:
        flash(f'Error: {str(e)}')
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
