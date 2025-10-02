#!/bin/bash

# 516 Hackers Captive Portal - iptables Rules
# FOR LAB USE ONLY

set -e

INTERFACE="wlan0"
GATEWAY="192.168.100.1"
PORTAL_PORT="5000"

echo "🔧 Setting up 516 Hackers iptables rules..."

# Flush existing rules
echo "🔄 Flushing existing rules..."
iptables -F
iptables -t nat -F
iptables -X
iptables -t nat -X

# Default policies
echo "⚙️ Setting default policies..."
iptables -P INPUT ACCEPT
iptables -P FORWARD DROP
iptables -P OUTPUT ACCEPT

# Allow established connections
echo "🔗 Allowing established connections..."
iptables -A FORWARD -i $INTERFACE -o eth0 -j ACCEPT
iptables -A FORWARD -i eth0 -o $INTERFACE -m state --state RELATED,ESTABLISHED -j ACCEPT

# NAT for internet sharing
echo "🌐 Setting up NAT..."
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# Captive portal redirect rules
echo "🎯 Setting up captive portal redirects..."

# Redirect HTTP to portal
iptables -t nat -A PREROUTING -i $INTERFACE -p tcp --dport 80 -j DNAT --to-destination $GATEWAY:$PORTAL_PORT
iptables -t nat -A PREROUTING -i $INTERFACE -p tcp --dport 443 -j DNAT --to-destination $GATEWAY:$PORTAL_PORT

# Allow DNS queries
echo "📡 Allowing DNS queries..."
iptables -A FORWARD -i $INTERFACE -p udp --dport 53 -j ACCEPT
iptables -A FORWARD -i $INTERFACE -p tcp --dport 53 -j ACCEPT

# Allow portal access
echo "🚪 Allowing portal access..."
iptables -A INPUT -i $INTERFACE -p tcp --dport $PORTAL_PORT -j ACCEPT
iptables -A INPUT -i $INTERFACE -p udp --dport $PORTAL_PORT -j ACCEPT

# Logging (optional)
echo "📝 Enabling logging..."
iptables -A FORWARD -i $INTERFACE -j LOG --log-prefix "516HACKERS_FORWARD: "
iptables -A INPUT -i $INTERFACE -j LOG --log-prefix "516HACKERS_INPUT: "

echo ""
echo "✅ 516 Hackers iptables rules configured!"
echo ""
echo "📋 Current rules:"
echo "NAT Rules:"
iptables -t nat -L -n
echo ""
echo "Forward Rules:"
iptables -L FORWARD -n
