from flask import Blueprint, request, session, jsonify
import hashlib
import time

auth_bp = Blueprint('auth', __name__)

# Insecure session storage for demonstration
sessions = {}

@auth_bp.route('/api/login', methods=['POST'])
def api_login():
    """Insecure API login for demonstration"""
    data = request.get_json()
    
    # Vulnerable: No input validation
    username = data.get('username')
    password = data.get('password')
    
    # Simple credential check (INSECURE)
    if username and password:
        # Create session (INSECURE - predictable session IDs)
        session_id = hashlib.md5(f"{username}{time.time()}".encode()).hexdigest()
        sessions[session_id] = {
            'username': username,
            'logged_in': True,
            'ip_address': request.remote_addr
        }
        
        return jsonify({
            'status': 'success',
            'session_id': session_id,
            'message': 'Login successful - 516 Hackers Demo'
        })
    
    return jsonify({'status': 'error', 'message': 'Login failed'})

@auth_bp.route('/api/secure-login', methods=['POST'])
def secure_login():
    """Secure login implementation for comparison"""
    data = request.get_json()
    
    # Secure input validation
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'status': 'error', 'message': 'Missing credentials'})
    
    # Rate limiting check
    client_ip = request.remote_addr
    login_attempts = sessions.get(f"attempts_{client_ip}", 0)
    
    if login_attempts > 5:
        return jsonify({'status': 'error', 'message': 'Too many attempts'})
    
    # Secure authentication logic would go here
    # For demo, we'll use a simple check
    if username == 'secureuser' and password == 'SecurePass123!':
        # Secure session creation
        import secrets
        session_token = secrets.token_urlsafe(32)
        
        sessions[session_token] = {
            'username': username,
            'logged_in': True,
            'ip_address': request.remote_addr,
            'user_agent': request.headers.get('User-Agent'),
            'created_at': time.time()
        }
        
        return jsonify({
            'status': 'success',
            'session_token': session_token,
            'secure': True,
            'message': 'Secure login successful'
        })
    
    # Track failed attempts
    sessions[f"attempts_{client_ip}"] = login_attempts + 1
    
    return jsonify({'status': 'error', 'message': 'Invalid credentials'})
