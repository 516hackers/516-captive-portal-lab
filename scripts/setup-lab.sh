#!/bin/bash

# 516 Hackers Captive Portal Lab Setup Script

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

# Setup Python virtual environment
echo "🐍 Setting up Python environment..."
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

# Build Docker images
echo "🐳 Building Docker containers..."
docker-compose build

# Download additional tools
echo "🔧 Downloading security tools..."
if [ ! -f "tools/session_hijack_tool.py" ]; then
    mkdir -p tools
    curl -o tools/session_hijack_tool.py https://raw.githubusercontent.com/516hackers/security-tools/main/session_hijack.py
fi

# Set permissions
echo "🔐 Setting file permissions..."
chmod +x network/setup-network.sh
chmod +x scripts/attack-simulator.py
chmod +x scripts/security-test.py

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
echo "   ./scripts/attack-simulator.py    - Run attack simulations"
echo "   ./scripts/security-test.py       - Security testing"
echo "   ./network/setup-network.sh       - Setup wireless network (requires sudo)"
echo ""
echo "⚠️  IMPORTANT:"
echo "   - Use only in isolated environments"
echo "   - Do not expose to the internet"
echo "   - For educational purposes only"
echo ""
echo "🔗 Portal will be available at: http://localhost:5000"
echo ""
echo "Built with ❤️ by 516 Hackers"
