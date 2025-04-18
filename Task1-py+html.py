from flask import Flask, request

app = Flask(__name__)

def caesar_encrypt(text, shift):
    return ''.join([chr((ord(char) + shift) % 256) for char in text])

def caesar_decrypt(text, shift):
    return ''.join([chr((ord(char) - shift) % 256) for char in text])

@app.route('/', methods=['GET', 'POST'])
def index():
    result = ''
    if request.method == 'POST':
        message = request.form['message']
        shift = int(request.form['shift']) % 256
        action = request.form['action']

        if action == 'encrypt':
            result = caesar_encrypt(message, shift)
        elif action == 'decrypt':
            result = caesar_decrypt(message, shift)

    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Caesar Cipher</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f0f0f0;
                padding: 40px;
            }}
            .container {{
                background-color: white;
                padding: 30px;
                max-width: 600px;
                margin: auto;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);
                border-radius: 10px;
            }}
            h1 {{
                text-align: center;
                color: #333;
            }}
            label {{
                font-weight: bold;
            }}
            textarea, input {{
                width: 100%;
                padding: 10px;
                margin-top: 5px;
                margin-bottom: 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
                box-sizing: border-box;
            }}
            button {{
                background-color: #007BFF;
                color: white;
                padding: 10px 20px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin-right: 10px;
            }}
            button:hover {{
                background-color: #0056b3;
            }}
            .result {{
                background-color: #f4f4f4;
                padding: 15px;
                border: 1px solid #ccc;
                border-radius: 5px;
                word-wrap: break-word;
                white-space: pre-wrap;
                margin-top: 20px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔐 Caesar Cipher Web App</h1>
            <form method="POST">
                <label>Message:</label><br>
                <textarea name="message" rows="4" required></textarea><br>

                <label>Shift Value (0-255):</label><br>
                <input type="number" name="shift" min="0" max="255" required><br>

                <button type="submit" name="action" value="encrypt">Encrypt</button>
                <button type="submit" name="action" value="decrypt">Decrypt</button>
            </form>

            {'<div class="result"><strong>Result:</strong><br>' + result + '</div>' if result else ''}
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(debug=True)
