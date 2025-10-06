
from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Demo credentials
USERS = {
    'guest': 'guest123',
    'admin': '516HackersSecure123'
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>516 Hackers Captive Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }
        .container { max-width: 400px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; background: #3498db; color: white; border: none; padding: 12px; border-radius: 5px; cursor: pointer; }
        button:hover { background: #2980b9; }
        .demo-creds { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 516 Hackers</h1>
            <p>Captive Portal Lab</p>
        </div>
        
        {% if session.authenticated %}
        <h2>Welcome, {{ session.username }}! 🎉</h2>
        <p>You have successfully authenticated to the 516 Hackers lab network.</p>
        <p><strong>Session Security Demo:</strong></p>
        <ul>
            <li>Session ID: {{ session.session_id[:10] }}...</li>
            <li>IP Address: {{ request.remote_addr }}</li>
        </ul>
        <a href="/logout"><button>Logout</button></a>
        {% else %}
        <h2>Network Authentication Required</h2>
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" value="guest" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" value="guest123" required>
            </div>
            <button type="submit">Connect to Network</button>
        </form>
        
        <div class="demo-creds">
            <h3>Demo Credentials:</h3>
            <p><strong>User:</strong> guest / guest123</p>
            <p><strong>Admin:</strong> admin / 516HackersSecure123</p>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if username in USERS and USERS[username] == password:
        session['authenticated'] = True
        session['username'] = username
        session['session_id'] = os.urandom(16).hex()
        return redirect('/')
    else:
        return "Invalid credentials - <a href='/'>Try again</a>"

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
