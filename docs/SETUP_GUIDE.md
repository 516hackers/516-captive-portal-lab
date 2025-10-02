
# 516 Hackers Captive Portal Lab - Setup Guide

## 🎯 Overview

This guide will help you set up the 516 Hackers Captive Portal Lab for security training and research.

## 📋 Prerequisites

### Hardware Requirements
- Linux machine (Ubuntu 20.04+ recommended)
- Wireless network adapter (supporting AP mode)
- Minimum 2GB RAM, 10GB disk space

### Software Requirements
- Docker Engine 20.10+
- Docker Compose 2.0+
- Python 3.8+
- Git

## 🚀 Quick Setup

### 1. Clone the Repository
```bash
git clone https://github.com/516hackers/516-captive-portal-lab.git
cd 516-captive-portal-lab
```

### 2. Run Automated Setup
```bash
chmod +x scripts/setup-lab.sh
./scripts/setup-lab.sh
```

### 3. Start the Lab
```bash
docker-compose up
```

### 4. Access the Portal
Open your browser to: `http://localhost:5000`

## 🔧 Advanced Setup

### Wireless Network Configuration

#### Option A: Automated Setup
```bash
sudo ./network/setup-network.sh
```

#### Option B: Manual Configuration

1. **Install dependencies**:
```bash
sudo apt update
sudo apt install hostapd dnsmasq iptables
```

2. **Configure hostapd** (`/etc/hostapd/hostapd.conf`):
```ini
interface=wlan0
driver=nl80211
ssid=516-Hackers-Lab
hw_mode=g
channel=6
wpa=2
wpa_passphrase=TrainingLab123
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

3. **Configure dnsmasq** (`/etc/dnsmasq.conf`):
```ini
interface=wlan0
dhcp-range=192.168.100.10,192.168.100.100,255.255.255.0,24h
dhcp-option=3,192.168.100.1
server=8.8.8.8
```

4. **Start services**:
```bash
sudo systemctl start hostapd
sudo systemctl start dnsmasq
```

### Docker Configuration

#### Customize Environment
Create `.env` file:
```bash
# 516 Hackers Lab Configuration
SECRET_KEY=your-secure-key-here
REDIS_URL=redis://portal-db:6379/0
FLASK_ENV=development
PORTAL_SSID=516-Hackers-Lab
```

#### Build Custom Images
```bash
docker-compose build --no-cache
docker-compose up -d
```

## 🧪 Testing the Setup

### 1. Verify Services
```bash
# Check running containers
docker-compose ps

# Check portal accessibility
curl http://localhost:5000

# Test wireless network
iwconfig wlan0
```

### 2. Run Security Tests
```bash
# Basic security scan
python scripts/security-test.py

# Attack simulation
python scripts/attack-simulator.py

# Network tests
ping 192.168.100.1
```

### 3. Connect Test Devices
1. Connect to WiFi: `516-Hackers-Lab`
2. Password: `TrainingLab123`
3. Open any HTTP website
4. Should redirect to captive portal

## 🛠️ Troubleshooting

### Common Issues

**Wireless adapter not found**:
```bash
# Check available interfaces
iwconfig

# Install drivers if needed
sudo apt install linux-firmware
```

**Docker permission errors**:
```bash
# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker
```

**Portal not redirecting**:
```bash
# Check iptables rules
sudo iptables -t nat -L

# Verify DNS configuration
nslookup google.com 192.168.100.1
```

**Rate limiting issues**:
```bash
# Reset Docker containers
docker-compose down
docker-compose up
```

### Logs and Monitoring

**View application logs**:
```bash
docker-compose logs portal-backend
docker-compose logs portal-db
```

**Network monitoring**:
```bash
# Monitor wireless clients
iw dev wlan0 station dump

# View DHCP leases
cat /var/lib/dhcp/dhcpd.leases
```

**Security monitoring**:
```bash
# View failed login attempts
grep "Failed login" logs/portal.log

# Monitor network traffic
sudo tcpdump -i wlan0
```

## 🔒 Security Considerations

### Lab Isolation
- Use dedicated hardware when possible
- Disconnect from production networks
- Regular environment resets
- Monitor for unexpected traffic

### Access Control
- Change default credentials
- Limit lab participant access
- Log all activities
- Regular security audits

### Safe Practices
- Never use real credentials
- Isolate lab network completely
- Regular vulnerability scanning
- Keep software updated

## 📞 Support

### Documentation
- [Lesson Plans](LESSONS.md)
- [Attack Scenarios](ATTACK_SCENARIOS.md)
- [API Documentation](API.md)

### Community
- GitHub Issues: Bug reports and feature requests
- 516 Hackers Forum: Community support
- Security Advisories: Vulnerability notifications

### Emergency Reset
```bash
# Complete lab reset
./scripts/reset-lab.sh

# Network reset
sudo systemctl restart networking

# Docker reset
docker system prune -a
```

---

**Need help?** Contact the 516 Hackers team through our GitHub repository.

*Built with ❤️ for the security community*
