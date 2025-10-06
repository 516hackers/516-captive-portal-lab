
from flask import Flask, render_template_string, request, redirect, session, url_for
import os

app = Flask(__name__)
app.secret_key = '516-hackers-cloud-shell-key'

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
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
        .header { background: #2c3e50; color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; text-align: center; }
        .warning { background: #e74c3c; color: white; padding: 10px; border-radius: 5px; margin-bottom: 15px; text-align: center; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input[type="text"], input[type="password"] { width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
        button { width: 100%; background: #3498db; color: white; border: none; padding: 12px; border-radius: 5px; cursor: pointer; font-size: 16px; }
        button:hover { background: #2980b9; }
        .demo-creds { background: #f8f9fa; padding: 15px; border-radius: 5px; margin-top: 20px; border-left: 4px solid #3498db; }
        .success { background: #27ae60; color: white; padding: 15px; border-radius: 5px; margin: 15px 0; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔐 516 Hackers</h1>
            <p>Captive Portal Security Lab</p>
        </div>
        
        <div class="warning">
            ⚠️ FOR EDUCATIONAL USE ONLY - CLOUD SHELL DEMO
        </div>
        
        {% if session.authenticated %}
        <div class="success">
            <h2>🎉 Authentication Successful!</h2>
            <p>Welcome, <strong>{{ session.username }}</strong>!</p>
        </div>
        
        <h3>Lab Environment Active</h3>
        <p><strong>Session ID:</strong> {{ session.session_id[:15] }}...</p>
        <p><strong>Your IP:</strong> {{ request.remote_addr }}</p>
        <p><strong>User Agent:</strong> {{ request.headers.get('User-Agent', 'Unknown')[:50] }}...</p>
        
        <div class="demo-creds">
            <h4>🔍 Security Demo Features:</h4>
            <ul>
                <li>Session Management</li>
                <li>Authentication Flow</li>
                <li>Form Security</li>
                <li>Network Isolation</li>
            </ul>
        </div>
        
        <a href="/logout"><button>🚪 Logout & Reset Session</button></a>
        
        {% else %}
        <h2>🔒 Network Authentication Required</h2>
        <p>Please login to access the 516 Hackers training network:</p>
        
        <form method="POST" action="/login">
            <div class="form-group">
                <label>Username:</label>
                <input type="text" name="username" value="guest" required>
            </div>
            <div class="form-group">
                <label>Password:</label>
                <input type="password" name="password" value="guest123" required>
            </div>
            <button type="submit">🔗 Connect to Lab Network</button>
        </form>
        
        <div class="demo-creds">
            <h3>🧪 Demo Credentials:</h3>
            <p><strong>Standard User:</strong><br>Username: <code>guest</code><br>Password: <code>guest123</code></p>
            <p><strong>Admin Access:</strong><br>Username: <code>admin</code><br>Password: <code>516HackersSecure123</code></p>
        </div>
        
        <div style="margin-top: 20px; padding: 15px; background: #fff3cd; border-radius: 5px;">
            <h4>📚 About This Lab:</h4>
            <p>This is a security training environment demonstrating captive portal vulnerabilities and protections.</p>
            <p><strong>Use responsibly in isolated environments only.</strong></p>
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
        return '''
        <div style="max-width: 500px; margin: 50px auto; padding: 20px; background: #e74c3c; color: white; border-radius: 10px; text-align: center;">
            <h2>❌ Authentication Failed</h2>
            <p>Invalid credentials provided.</p>
            <a href="/" style="color: white; text-decoration: underline;">Try Again</a>
        </div>
        '''

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
