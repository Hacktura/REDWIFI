#!/bin/bash

# Red WiFi Installation Script
# Installs all dependencies and configures the framework

echo "================================"
echo "  Red WiFi v2.0 Setup Script"
echo "================================"

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root (use: sudo bash setup.sh)"
   exit 1
fi

echo "[*] Updating package lists..."
apt-get update

echo "[*] Installing system dependencies..."
apt-get install -y \
    python3 \
    python3-pip \
    build-essential \
    libssl-dev \
    libffi-dev \
    git

echo "[*] Installing aircrack-ng suite..."
apt-get install -y \
    aircrack-ng \
    airodump-ng \
    aireplay-ng \
    aircrack-ng

echo "[*] Installing hashcat..."
apt-get install -y hashcat

echo "[*] Installing John the Ripper..."
apt-get install -y john

echo "[*] Installing additional tools..."
apt-get install -y \
    cowpatty \
    reaver \
    pixiewps \
    hcxtools \
    hcxdumptool \
    tcpdump

echo "[*] Installing Python dependencies..."
pip3 install -r requirements.txt

echo "[*] Installing Red WiFi package..."
pip3 install -e .

echo "[*] Downloading wordlists..."
mkdir -p /opt/wordlists
cd /opt/wordlists

# Download rockyou.txt if not present
if [ ! -f rockyou.txt ]; then
    echo "Downloading rockyou.txt (this may take a while)..."
    wget -q https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Common-Credentials/10-million-password-list-top-1000000.txt -O rockyou.txt
fi

echo "[+] Installation complete!"
echo ""
echo "Usage:"
echo "  red-wifi scan --interface wlan0"
echo "  red-wifi auto --interface wlan0"
echo "  red-wifi --help"
echo ""
echo "First, set your WiFi adapter to monitor mode:"
echo "  red-wifi monitor wlan0"
echo ""
