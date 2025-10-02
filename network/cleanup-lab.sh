#!/bin/bash

# 516 Hackers Captive Portal Lab - Cleanup Script

set -e

echo "🧹 516 Hackers Lab Cleanup"

# Stop services
echo "🛑 Stopping services..."
pkill hostapd 2>/dev/null || true
pkill dnsmasq 2>/dev/null || true
systemctl stop dnsmasq 2>/dev/null || true

# Reset network interface
echo "🔁 Resetting network interface..."
INTERFACE="wlan0"
ip addr flush dev $INTERFACE 2>/dev/null || true
ip link set $INTERFACE down 2>/dev/null || true
iwconfig $INTERFACE mode managed 2>/dev/null || true
ip link set $INTERFACE up 2>/dev/null || true

# Clean iptables
echo "🧹 Cleaning iptables..."
./network/iptables-cleanup.sh

# Restart network services
echo "🔁 Restarting network services..."
systemctl start NetworkManager 2>/dev/null || true
systemctl start systemd-resolved 2>/dev/null || true

echo ""
echo "✅ 516 Hackers Lab cleanup complete!"
echo "Network interface $INTERFACE has been reset to normal operation."
