from flask import Flask, render_template, session, redirect, url_for, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import redis
import logging
from config import config

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('516-captive-portal')

app = Flask(__name__)
app.config.from_object(config['development'])

# Rate limiting
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri=app.config['RATELIMIT_STORAGE_URL']
)

# Redis for session storage
redis_client = redis.Redis.from_url(app.config['REDIS_URL'], decode_responses=True)

@app.before_request
def set_security_headers():
    """Set security headers for all responses"""
    for header, value in app.config['SECURITY_HEADERS'].items():
        app.make_response(render_template('base.html')).headers[header] = value

@app.route('/')
def index():
    """516 Hackers Portal Landing Page"""
    if session.get('authenticated'):
        return redirect(url_for('portal'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
@limiter.limit("10 per minute")
def login():
    """Login endpoint with security demonstrations"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Insecure authentication for demonstration
        if username == 'guest' and password == 'guest123':
            session['authenticated'] = True
            session['username'] = username
            session['user_ip'] = request.remote_addr
            
            # Log the login attempt
            logger.info(f"User {username} logged in from {request.remote_addr}")
            
            return redirect(url_for('portal'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/portal')
def portal():
    """Main portal page after authentication"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    return render_template('portal.html', 
                         username=session.get('username'),
                         user_ip=session.get('user_ip'))

@app.route('/hijack-demo')
def hijack_demo():
    """Session hijacking demonstration page"""
    return render_template('hijack_demo.html')

@app.route('/admin')
def admin():
    """Admin panel for lab management"""
    if session.get('username') != 'admin':
        return "Access Denied - 516 Hackers Admin Only", 403
    
    # Get session statistics
    active_sessions = redis_client.keys('session:*')
    return render_template('admin.html', 
                         active_sessions=len(active_sessions))

@app.route('/logout')
def logout():
    """Secure logout with session cleanup"""
    session.clear()
    return redirect(url_for('index'))

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(429)
def ratelimit_handler(error):
    return render_template('429.html'), 429

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=app.config['PORT'], debug=True)
