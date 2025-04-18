from flask import Flask, render_template_string, request, jsonify
import re

app = Flask(__name__)

# HTML template with JavaScript for real-time password checking
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Password Strength Checker</title>
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
        input[type="password"] {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
            margin-bottom: 10px;
        }
        .strength-meter {
            margin-top: 20px;
        }
        .criteria {
            margin-top: 20px;
        }
        .criteria-item {
            margin: 5px 0;
        }
        .check {
            color: #4CAF50;
        }
        .x-mark {
            color: #f44336;
        }
        .score {
            font-size: 24px;
            text-align: center;
            margin: 20px 0;
        }
        .strength-text {
            text-align: center;
            font-size: 20px;
            margin-bottom: 10px;
        }
        .very-strong { color: #4CAF50; }
        .strong { color: #2196F3; }
        .moderate { color: #FF9800; }
        .weak { color: #f44336; }
        .suggestions {
            margin-top: 20px;
            padding: 10px;
            border-radius: 4px;
            background-color: #fff3cd;
            color: #856404;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Password Strength Checker</h1>
        
        <div class="form-group">
            <label for="password">Enter Password:</label>
            <input type="password" id="password" oninput="checkPassword()" placeholder="Type your password">
        </div>

        <div class="strength-meter">
            <div class="strength-text" id="strengthText"></div>
            <div class="score" id="score"></div>
        </div>

        <div class="criteria">
            <div class="criteria-item" id="lengthCheck">
                <span class="x-mark">✗</span> Length (8+ characters)
            </div>
            <div class="criteria-item" id="uppercaseCheck">
                <span class="x-mark">✗</span> Uppercase letters
            </div>
            <div class="criteria-item" id="lowercaseCheck">
                <span class="x-mark">✗</span> Lowercase letters
            </div>
            <div class="criteria-item" id="numberCheck">
                <span class="x-mark">✗</span> Numbers
            </div>
            <div class="criteria-item" id="specialCheck">
                <span class="x-mark">✗</span> Special characters
            </div>
        </div>

        <div class="suggestions" id="suggestions"></div>
    </div>

    <script>
        function checkPassword() {
            const password = document.getElementById('password').value;
            
            fetch('/check', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({password: password})
            })
            .then(response => response.json())
            .then(data => {
                updateUI(data);
            });
        }

        function updateUI(data) {
            // Update strength text and color
            const strengthText = document.getElementById('strengthText');
            strengthText.textContent = data.strength;
            strengthText.className = 'strength-text ' + data.strength.toLowerCase().replace(' ', '-');

            // Update score
            document.getElementById('score').textContent = data.score + '/100';

            // Update criteria checks
            updateCriteriaCheck('lengthCheck', data.length >= 8);
            updateCriteriaCheck('uppercaseCheck', data.has_uppercase);
            updateCriteriaCheck('lowercaseCheck', data.has_lowercase);
            updateCriteriaCheck('numberCheck', data.has_numbers);
            updateCriteriaCheck('specialCheck', data.has_special);

            // Update suggestions
            const suggestionsDiv = document.getElementById('suggestions');
            if (data.feedback.length > 0) {
                suggestionsDiv.innerHTML = '<strong>Suggestions:</strong><br>' + 
                    data.feedback.join('<br>');
                suggestionsDiv.style.display = 'block';
            } else {
                suggestionsDiv.style.display = 'none';
            }
        }

        function updateCriteriaCheck(elementId, isValid) {
            const element = document.getElementById(elementId);
            const checkmark = element.getElementsByTagName('span')[0];
            if (isValid) {
                checkmark.textContent = '✓';
                checkmark.className = 'check';
            } else {
                checkmark.textContent = '✗';
                checkmark.className = 'x-mark';
            }
        }
    </script>
</body>
</html>
'''

def check_password_strength(password):
    """
    Assess the strength of a password based on various criteria.
    Returns a dictionary containing the assessment results.
    """
    assessment = {
        'length': len(password),
        'has_uppercase': bool(re.search(r'[A-Z]', password)),
        'has_lowercase': bool(re.search(r'[a-z]', password)),
        'has_numbers': bool(re.search(r'\d', password)),
        'has_special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password)),
        'score': 0,
        'feedback': []
    }

    # Score calculation (out of 100)
    if assessment['length'] >= 12:
        assessment['score'] += 40
    elif assessment['length'] >= 8:
        assessment['score'] += 25
    elif assessment['length'] >= 6:
        assessment['score'] += 10

    if assessment['has_uppercase']: assessment['score'] += 15
    if assessment['has_lowercase']: assessment['score'] += 15
    if assessment['has_numbers']: assessment['score'] += 15
    if assessment['has_special']: assessment['score'] += 15

    # Generate feedback
    if assessment['length'] < 8:
        assessment['feedback'].append("Password is too short. Use at least 8 characters.")
    if not assessment['has_uppercase']:
        assessment['feedback'].append("Add uppercase letters (A-Z).")
    if not assessment['has_lowercase']:
        assessment['feedback'].append("Add lowercase letters (a-z).")
    if not assessment['has_numbers']:
        assessment['feedback'].append("Add numbers (0-9).")
    if not assessment['has_special']:
        assessment['feedback'].append("Add special characters (!@#$%^&*(),.?\":{}|<>).")

    # Overall strength assessment
    if assessment['score'] >= 90:
        assessment['strength'] = 'Very Strong'
    elif assessment['score'] >= 70:
        assessment['strength'] = 'Strong'
    elif assessment['score'] >= 50:
        assessment['strength'] = 'Moderate'
    else:
        assessment['strength'] = 'Weak'

    return assessment

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/check', methods=['POST'])
def check_password():
    data = request.get_json()
    password = data.get('password', '')
    return jsonify(check_password_strength(password))

if __name__ == '__main__':
    app.run(debug=True) 