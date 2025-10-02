#!/bin/bash

# 516 Hackers Captive Portal Network Setup Script
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
systemctl stop NetworkManager
systemctl stop wpa_supplicant

# Configure hostapd
echo "📝 Configuring hostapd..."
cat > /etc/hostapd/hostapd.conf << EOF
# 516 Hackers Lab Configuration
interface=$INTERFACE
driver=nl80211
ssid=$SSID
hw_mode=g
channel=$CHANNEL
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=$WPA_PASSPHRASE
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
EOF

# Configure dnsmasq
echo "📝 Configuring dnsmasq..."
cat > /etc/dnsmasq.conf << EOF
# 516 Hackers Lab DNS Configuration
interface=$INTERFACE
dhcp-range=192.168.100.10,192.168.100.100,255.255.255.0,24h
dhcp-option=3,$GATEWAY
dhcp-option=6,$GATEWAY
server=8.8.8.8
log-queries
log-dhcp
address=/516hackers.org/$GATEWAY
EOF

# Configure network interface
echo "🌐 Setting up network interface..."
ip addr add $GATEWAY/24 dev $INTERFACE
ip link set $INTERFACE up

# Configure iptables for NAT and redirect
echo "🔧 Configuring iptables rules..."
iptables -t nat -F
iptables -F

# NAT for internet sharing
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i $INTERFACE -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o $INTERFACE -m state --state RELATED,ESTABLISHED -j ACCEPT

# Redirect all HTTP traffic to portal
iptables -t nat -A PREROUTING -i $INTERFACE -p tcp --dport 80 -j DNAT --to-destination $GATEWAY:$PORTAL_PORT
iptables -t nat -A PREROUTING -i $INTERFACE -p tcp --dport 443 -j DNAT --to-destination $GATEWAY:$PORTAL_PORT

echo "🚀 Starting services..."
systemctl start hostapd
systemctl start dnsmasq

echo ""
echo "✅ 516 Hackers Captive Portal Lab Setup Complete!"
echo ""
echo "📶 Network: $SSID"
echo "🔑 Password: $WPA_PASSPHRASE"
echo "🌐 Portal: http://$GATEWAY:$PORTAL_PORT"
echo ""
echo "💡 Connect to WiFi network '$SSID' and open any HTTP website"
echo "⚠️  Remember: This is for educational use only!"
