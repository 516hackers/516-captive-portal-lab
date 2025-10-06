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

# Create simple backend files without heredoc
echo "⚙️ Creating essential backend files..."

# Create backend/requirements.txt with echo
echo "Flask==2.3.3
redis==4.6.0
requests==2.31.0" > backend/requirements.txt

# Create minimal backend/app.py
cat > backend/app.py << 'APPDONE'
from flask import Flask
app = Flask(__name__)
@app.route('/')
def home():
    return "516 Hackers Portal - Running!"
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
APPDONE

# Create backend/Dockerfile
cat > backend/Dockerfile << 'DOCKERDONE'
FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
DOCKERDONE

# Set permissions
echo "🔐 Setting file permissions..."
chmod +x network/setup-network.sh 2>/dev/null || true
chmod +x network/cleanup-lab.sh 2>/dev/null || true
chmod +x network/iptables-rules.sh 2>/dev/null || true
chmod +x network/iptables-cleanup.sh 2>/dev/null || true
chmod +x scripts/attack-simulator.py 2>/dev/null || true
chmod +x scripts/security-test.py 2>/dev/null || true

echo ""
echo "🎉 516 Hackers Lab Setup Complete!"
echo ""
echo "🚀 To start the lab:"
echo "   docker-compose up"
echo ""
echo "🔗 Portal will be available at: http://localhost:5000"
echo ""
echo "Built with ❤️ by 516 Hackers"
