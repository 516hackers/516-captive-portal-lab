# 🔐 516 Hackers Captive Portal Lab

> **⚠️ FOR SECURITY TRAINING ONLY - ISOLATED LAB USE ⚠️**

A modular captive portal lab demonstrating wireless security, session management, and authentication vulnerabilities.

## 🚀 Quick Start

### Prerequisites
- Linux with wireless adapter
- Docker & Docker Compose
- Python 3.8+

### 1. Clone & Setup
```bash
git clone https://github.com/516hackers/516-captive-portal-lab.git
cd 516-captive-portal-lab

# Run automated setup
chmod +x scripts/setup-lab.sh
./scripts/setup-lab.sh
```

### 2. Start Lab
```bash
# Start core services
docker-compose up --build

# Access portal: http://localhost:5000
```

### 3. Setup Wireless (Optional)
```bash
# Create access point
sudo ./network/setup-network.sh

# Connect to WiFi: "516-Hackers-Lab"
# Password: "TrainingLab123"
```

## 🎯 Lab Modules

### 1. Session Security
- Secure vs insecure session handling
- Session fixation attacks
- Token-based authentication

### 2. Authentication
- CSRF protection mechanisms
- Rate limiting implementation
- Secure form handling

### 3. Network Security
- MAC address filtering
- HTTPS enforcement
- DNS hijacking detection

### 4. Portal Bypass
- DNS manipulation techniques
- Proxy detection evasion
- Certificate pinning

## 🧪 Testing & Attacks

### Run Security Tests
```bash
# Comprehensive security audit
python scripts/security-test.py --audit

# Specific vulnerability tests
python scripts/attack-simulator.py --test csrf
python scripts/attack-simulator.py --test session
```

### Demo Credentials
```
Username: guest
Password: guest123

Admin: admin / 516HackersSecure123
```

## ⚙️ Configuration

### Network Settings
Edit `network/hostapd.conf`:
```ini
ssid=516-Hackers-Lab
channel=6
wpa_passphrase=TrainingLab123
```

### Portal Settings
Edit `backend/config.py`:
```python
PORTAL_CONFIG = {
    'ssid': '516-Hackers-Lab',
    'session_timeout': 3600,
    'max_devices': 10
}
```

## 🔧 Management

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f
```

### Reset Lab
```bash
# Complete reset
docker-compose down -v
docker system prune -a
./scripts/setup-lab.sh
```

## 🛡️ Security Features

### Secure Implementations
- ✅ HTTPS enforcement
- ✅ CSRF token validation
- ✅ Secure session management
- ✅ Rate limiting
- ✅ Input sanitization

### Vulnerable Implementations (for education)
- ❌ Session fixation
- ❌ CSRF vulnerabilities
- ❌ Weak authentication
- ❌ Insecure redirects

## 📚 Learning Path

### Beginner
- Basic portal concepts
- Secure login forms
- Session management

### Intermediate
- CSRF attacks & prevention
- Session hijacking
- Network protections

### Advanced
- Portal bypass methods
- Wireless security protocols
- Advanced persistence

## ⚠️ Safety Notice

**CRITICAL: FOR LAB USE ONLY**

- 🚫 **NEVER** deploy on production networks
- 🚫 **NEVER** expose to internet
- ✅ **ONLY** use in isolated environments
- ✅ **ONLY** for legitimate security training

## 🐛 Troubleshooting

### Common Issues
```bash
# Wireless adapter not found
iwconfig
sudo apt install linux-firmware

# Docker permissions
sudo usermod -aG docker $USER
newgrp docker

# Portal not redirecting
sudo iptables -t nat -L
```

### View Logs
```bash
docker-compose logs portal-backend
docker-compose logs portal-db
```

## 🤝 Contributing

We welcome contributions! See our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## 📄 License

Educational Use License - See [LICENSE](LICENSE) for details.

---

**Built with ❤️ by 516 Hackers for the security community**

*Need help? Check our [docs](docs/) or create an issue.*
