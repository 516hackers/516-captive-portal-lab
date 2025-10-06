
set -e

echo "🎯 516 Hackers Captive Portal Lab Setup"
echo "========================================"

# Check dependencies
echo "🔍 Checking dependencies..."

check_dependency() {
    if ! command -v $1 &> /dev/null; then
        echo "❌ $1 is not installed"
        return 1
    fi
    echo "✅ $1 found"
}

check_dependency docker
check_dependency docker-compose
check_dependency python3
check_dependency git

# Create necessary directories
echo "📁 Creating lab directories..."
mkdir -p logs
mkdir -p data
mkdir -p captures
mkdir -p backend/uploads
mkdir -p backend/secure-uploads

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies if requirements.txt exists
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
else
    echo "⚠️ requirements.txt not found, installing default packages..."
    pip install Flask redis requests
fi

# Build Docker images
echo "🐳 Building Docker containers..."
docker-compose build

# Create missing configuration files
echo "⚙️ Creating configuration files..."

# Create backend/requirements.txt if missing
if [ ! -f "backend/requirements.txt" ]; then
    cat > backend/requirements.txt << 'EOF'
Flask==2.3.3
Werkzeug==2.3.7
redis==4.6.0
requests==2.31.0
pycryptodome==3.18.0
Flask-Limiter==3.3.0
Flask-WTF==1.1.1
WTForms==3.0.1
python-dotenv==1.0.0
EOF
fi

# Create backend/config.py if missing
if [ ! -f "backend/config.py" ]; then
    cat > backend/config.py << 'EOF'
import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', '516-hackers-insecure-key-for-lab')
    PORT = int(os.environ.get('PORT', 5000))
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=60)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    
    PORTAL_CONFIG = {
        'ssid': '516-Hackers-Lab',
        'welcome_message': '516 Hackers Security Training Portal',
        'redirect_url': 'https://516hackers.org',
        'session_timeout': 3600,
        'max_devices': 10,
        'admin_email': 'admin@516hackers.org'
    }
    
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block'
    }

config = {
    'development': Config,
    'default': Config
}
EOF
fi

# Set permissions
echo "🔐 Setting file permissions..."
chmod +x network/setup-network.sh 2>/dev/null || true
chmod +x network/cleanup-lab.sh 2>/dev/null || true
chmod +x network/iptables-rules.sh 2>/dev/null || true
chmod +x network/iptables-cleanup.sh 2>/dev/null || true
chmod +x scripts/attack-simulator.py 2>/dev/null || true
chmod +x scripts/security-test.py 2>/dev/null || true

# Create lab configuration
echo "⚙️ Creating lab configuration..."
cat > lab.config << EOF
# 516 Hackers Lab Configuration
LAB_NAME="516 Hackers Captive Portal Lab"
LAB_VERSION="1.0"
LAB_MODE="training"
NETWORK_SSID="516-Hackers-Lab"
PORTAL_URL="http://localhost:5000"
ADMIN_USERNAME="admin"
ADMIN_PASSWORD="516HackersSecure123"
SECURITY_LEVEL="training"
EOF

echo ""
echo "🎉 516 Hackers Lab Setup Complete!"
echo ""
echo "🚀 To start the lab:"
echo "   docker-compose up"
echo ""
echo "📚 Available commands:"
echo "   python scripts/attack-simulator.py    - Run attack simulations"
echo "   python scripts/security-test.py       - Security testing"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Use only in isolated environments"
echo "   - Do not expose to the internet"
echo "   - For educational purposes only"
echo ""
echo "🔗 Portal will be available at: http://localhost:5000"
echo ""
echo "Built with ❤️ by 516 Hackers"
