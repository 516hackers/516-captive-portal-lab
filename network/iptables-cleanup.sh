#!/bin/bash

# 516 Hackers - iptables Cleanup Script

echo "🧹 Cleaning up 516 Hackers iptables rules..."

# Flush all rules
iptables -F
iptables -t nat -F
iptables -X
iptables -t nat -X

# Reset policies to default
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT

echo "✅ iptables rules cleaned up!"
