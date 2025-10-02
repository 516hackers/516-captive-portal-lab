# 🔐 516 Hackers Captive Portal Lab

> **⚠️ FOR SECURITY TRAINING ONLY - ISOLATED LAB USE ⚠️**

A complete captive portal laboratory for learning wireless security, session management, and authentication vulnerabilities.

## 🚀 Quick Start (5 minutes)

### 1. Clone & Setup
```bash
git clone https://github.com/516hackers/516-captive-portal-lab.git
cd 516-captive-portal-lab

# Set permissions and setup
chmod +x scripts/setup-lab.sh
./scripts/setup-lab.sh
```

### 2. Start Services
```bash
# Start the portal
docker-compose up --build

# Access: http://localhost:5000
```

### 3. Test Connection
- **Username**: `guest`
- **Password**: `guest123`
- Open any HTTP website to test redirect

## 🛠️ Complete Setup Guide

### Step 1: Prerequisites
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose python3 git

# Start Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

### Step 2: Clone Repository
```bash
git clone https://github.com/516hackers/516-captive-portal-lab.git
cd 516-captive-portal-lab
```

### Step 3: Run Automated Setup
```bash
# Make scripts executable
chmod +x scripts/setup-lab.sh
chmod +x network/*.sh

# Run setup
./scripts/setup-lab.sh
```

### Step 4: Start Portal Services
```bash
# Start all services
docker-compose up --build

# Or run in background
docker-compose up -d
```

### Step 5: Wireless Setup (Optional)
```bash
# Create access point
sudo ./network/setup-network.sh

# Connect devices to:
# SSID: 516-Hackers-Lab
# Password: TrainingLab123
```

## 🎯 Lab Modules

### 1. Session Security
- Secure vs insecure session handling
- Session fixation attacks
- Token-based authentication

**Demo**: Try session hijacking with fixed session IDs

### 2. Authentication
- CSRF protection mechanisms
- Rate limiting implementation
- Secure form handling

**Demo**: Test CSRF vulnerabilities in login forms

### 3. Network Security
- MAC address filtering
- HTTPS enforcement
- DNS hijacking detection

**Demo**: Analyze network traffic and DNS queries

### 4. Portal Bypass
- DNS manipulation techniques
- Proxy detection evasion
- Certificate pinning

**Demo**: Attempt to bypass portal authentication

## 🧪 Testing & Attacks

### Run Security Tests
```bash
# Comprehensive security audit
python scripts/security-test.py --audit

# Specific vulnerability tests
python scripts/attack-simulator.py --test csrf
python scripts/attack-simulator.py --test session
python scripts/attack-simulator.py --test sql
```

### Demo Credentials
```
Standard User:
Username: guest
Password: guest123

Admin Access:
Username: admin  
Password: 516HackersSecure123
```

## ⚙️ Configuration

### Network Settings
Edit `network/hostapd.conf`:
```ini
interface=wlan0
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
    'max_devices': 10,
    'admin_email': 'admin@516hackers.org'
}
```

## 🔧 Management Commands

### Start/Stop Services
```bash
# Start all services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f portal-backend

# Restart specific service
docker-compose restart portal-backend
```

### Network Management
```bash
# Setup wireless network
sudo ./network/setup-network.sh

# Cleanup network
sudo ./network/cleanup-lab.sh

# Check connected clients
iw dev wlan0 station dump
```

### Reset Lab
```bash
# Complete environment reset
docker-compose down -v
docker system prune -f
./scripts/setup-lab.sh
```

## 🛡️ Security Features

### Secure Implementations
- ✅ HTTPS enforcement
- ✅ CSRF token validation
- ✅ Secure session management
- ✅ Rate limiting
- ✅ Input sanitization
- ✅ Secure headers

### Vulnerable Implementations (for education)
- ❌ Session fixation
- ❌ CSRF vulnerabilities  
- ❌ Weak authentication
- ❌ Insecure redirects
- ❌ Cookie mishandling

## 📚 Learning Path

### Beginner (30 minutes)
1. Understand captive portal concepts
2. Practice secure login forms
3. Learn session management basics
4. Run basic security tests

### Intermediate (2 hours)
1. CSRF attacks & prevention
2. Session hijacking techniques
3. Network-level protections
4. Analyze attack simulations

### Advanced (4+ hours)
1. Portal bypass methods
2. Wireless security protocols
3. Advanced persistence attacks
4. Custom exploit development

## 🐛 Troubleshooting

### Common Issues

**Wireless adapter not found:**
```bash
# Check available interfaces
iwconfig

# Install drivers
sudo apt install linux-firmware

# Check USB devices
lsusb | grep -i wireless
```

**Docker permission errors:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Restart Docker service
sudo systemctl restart docker
```

**Portal not redirecting:**
```bash
# Check iptables rules
sudo iptables -t nat -L

# Verify DNS configuration
nslookup google.com 192.168.100.1

# Check service status
docker-compose ps
```

**Services not starting:**
```bash
# Check logs
docker-compose logs portal-backend
docker-compose logs portal-db

# Rebuild containers
docker-compose build --no-cache
```

### View Logs
```bash
# Application logs
docker-compose logs -f portal-backend

# Database logs  
docker-compose logs -f portal-db

# Security monitor
docker-compose logs -f security-monitor

# System logs
journalctl -u hostapd
journalctl -u dnsmasq
```

## ⚠️ Safety & Legal

### Critical Requirements
- 🚫 **NEVER** deploy on production networks
- 🚫 **NEVER** expose to the internet
- 🚫 **NEVER** use real/sensitive data
- ✅ **ONLY** use in isolated environments
- ✅ **ONLY** for legitimate security training
- ✅ **ALWAYS** obtain proper authorization

### Lab Isolation
```bash
# Recommended isolation methods
- Dedicated hardware
- Air-gapped networks  
- VLAN segmentation
- Physical disconnection
```

## 🤝 Contributing

We welcome contributions from the security community:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

See our [Contributing Guide](docs/CONTRIBUTING.md) for details.

## 📄 License

Educational Use License - See [LICENSE](LICENSE) for details.

## 🆘 Support

### Documentation
- [Setup Guide](docs/SETUP_GUIDE.md)
- [Lesson Plans](docs/LESSONS.md) 
- [Attack Scenarios](docs/ATTACK_SCENARIOS.md)

### Community
- GitHub Issues: Bug reports and feature requests
- 516 Hackers Forum: Community support and discussions

### Emergency Reset
```bash
# Complete lab reset
./scripts/reset-lab.sh

# Network reset  
sudo ./network/cleanup-lab.sh

# Docker reset
docker system prune -af
```

---

**Built with ❤️ by 516 Hackers for the security community**

*"Knowledge is power, but responsibility is key"*

**Need help?** Check our [documentation](docs/) or create an issue on GitHub.
