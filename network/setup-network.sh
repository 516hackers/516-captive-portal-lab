#!/bin/bash

# 516 Hackers Captive Portal Lab - Network Setup Script
# FOR LAB USE ONLY

set -e

echo "🔧 516 Hackers Captive Portal Lab - Network Setup"
echo "⚠️  RUN THIS SCRIPT WITH SUDO PRIVILEGES"
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root: sudo $0"
    exit 1
fi

# Configuration
INTERFACE="wlan0"
SSID="516-Hackers-Lab"
CHANNEL="6"
WPA_PASSPHRASE="TrainingLab123"
IP_RANGE="192.168.100.0/24"
GATEWAY="192.168.100.1"
PORTAL_PORT="5000"

echo "📡 Setting up captive portal network..."
echo "SSID: $SSID"
echo "IP Range: $IP_RANGE"
echo "Gateway: $GATEWAY"
echo ""

# Check for wireless interface
if ! iwconfig $INTERFACE > /dev/null 2>&1; then
    echo "❌ Wireless interface $INTERFACE not found"
    echo "Available interfaces:"
    iwconfig | grep -v "no wireless" | cut -d' ' -f1
    exit 1
fi

# Stop conflicting services
echo "🛑 Stopping network services..."
systemctl stop NetworkManager 2>/dev/null || true
systemctl stop wpa_supplicant 2>/dev/null || true
systemctl stop systemd-resolved 2>/dev/null || true

# Kill any existing hostapd or dnsmasq processes
echo "🔪 Killing existing processes..."
pkill hostapd 2>/dev/null || true
pkill dnsmasq 2>/dev/null || true

# Configure hostapd
echo "📝 Configuring hostapd..."
cp network/hostapd.conf /etc/hostapd/hostapd.conf
chmod 644 /etc/hostapd/hostapd.conf

# Configure dnsmasq
echo "📝 Configuring dnsmasq..."
cp network/dnsmasq.conf /etc/dnsmasq.conf
chmod 644 /etc/dnsmasq.conf

# Configure network interface
echo "🌐 Setting up network interface..."
# Bring down interface
ip link set $INTERFACE down 2>/dev/null || true
# Set to managed mode
iwconfig $INTERFACE mode managed 2>/dev/null || true
# Bring up interface
ip link set $INTERFACE up
# Set IP address
ip addr flush dev $INTERFACE 2>/dev/null || true
ip addr add $GATEWAY/24 dev $INTERFACE

# Configure iptables for captive portal
echo "🔧 Configuring iptables rules..."
chmod +x network/iptables-rules.sh
./network/iptables-rules.sh

# Enable IP forwarding
echo "🔄 Enabling IP forwarding..."
echo 1 > /proc/sys/net/ipv4/ip_forward
sysctl -w net.ipv4.ip_forward=1

# Start services
echo "🚀 Starting services..."

# Start hostapd in background
echo "📶 Starting hostapd..."
hostapd -B /etc/hostapd/hostapd.conf

# Start dnsmasq
echo "🌐 Starting dnsmasq..."
systemctl start dnsmasq

# Wait for services to start
sleep 3

# Verify services are running
echo "🔍 Verifying services..."
if pgrep hostapd > /dev/null; then
    echo "✅ hostapd is running"
else
    echo "❌ hostapd failed to start"
    exit 1
fi

if pgrep dnsmasq > /dev/null; then
    echo "✅ dnsmasq is running"
else
    echo "❌ dnsmasq failed to start"
    exit 1
fi

# Show network status
echo ""
echo "📊 Network Status:"
echo "Interface: $INTERFACE"
echo "IP Address: $(ip addr show $INTERFACE | grep 'inet ' | awk '{print $2}')"
echo "SSID: $SSID"
echo "Channel: $CHANNEL"

# Show iptables rules
echo ""
echo "🛡️ iptables Rules Summary:"
iptables -t nat -L PREROUTING -n | grep "516"
iptables -L FORWARD -n | grep "ACCEPT"

echo ""
echo "✅ 516 Hackers Captive Portal Lab Setup Complete!"
echo ""
echo "🎯 Next Steps:"
echo "   1. Start the portal: docker-compose up"
echo "   2. Connect to WiFi: $SSID"
echo "   3. Password: $WPA_PASSPHRASE"
echo "   4. Open any website to test redirect"
echo ""
echo "📡 Network Info:"
echo "   WiFi: $SSID"
echo "   Password: $WPA_PASSPHRASE"
echo "   Portal: http://$GATEWAY:$PORTAL_PORT"
echo ""
echo "⚠️  Safety Reminder:"
echo "   - FOR EDUCATIONAL USE ONLY"
echo "   - ISOLATED LAB ENVIRONMENT"
echo "   - DO NOT EXPOSE TO INTERNET"
echo ""
echo "🔧 Troubleshooting:"
echo "   View logs: docker-compose logs"
echo "   Reset: ./network/iptables-cleanup.sh"
echo "   Check clients: iw dev $INTERFACE station dump"
echo ""
echo "Built with ❤️ by 516 Hackers"
