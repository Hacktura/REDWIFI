# Getting Started with Red WiFi

## Table of Contents
1. [Requirements](#requirements)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Quick Start](#quick-start)
5. [Troubleshooting](#troubleshooting)

## Requirements

### Operating System
- Linux (Ubuntu 18.04+, Kali Linux, Debian, etc.)
- Root/sudo access required for WiFi operations
- 2GB minimum RAM, 4GB+ recommended

### Hardware
- Computer with WiFi adapter
- Monitor mode capable adapter (see [Compatible Hardware](#compatible-hardware))

### Software Dependencies
- Python 3.8 or higher
- pip3 package manager
- aircrack-ng suite
- hashcat or John the Ripper

### Compatible Hardware

#### Recommended Adapters
- Alfa AWUS036ACH - Professional standard, excellent range
- TP-Link TL-WN722N - Budget-friendly, widely available
- Netgear WNDA3100v2 - Good range, reliable

#### Minimum Requirements
- Support for monitor mode
- Support for packet injection
- Ralink, Atheros, or Broadcom chipset

Check compatibility:
```bash
iwconfig  # List interfaces
sudo airmon-ng  # Check monitor mode support
```

## Installation

### Method 1: Automated Setup (Recommended)

```bash
# Clone repository
git clone https://github.com/redwifi/red-wifi.git
cd red-wifi

# Run automated setup (requires sudo)
sudo bash setup.sh

# Verify installation
python3 -m pytest tests/
```

### Method 2: Manual Installation

```bash
# 1. Install system dependencies
sudo apt-get update
sudo apt-get install -y python3 python3-pip aircrack-ng hashcat john

# 2. Clone repository
git clone https://github.com/redwifi/red-wifi.git
cd red-wifi

# 3. Install Python dependencies
pip3 install -r requirements.txt

# 4. Install Red WiFi
pip3 install -e .

# 5. Download wordlists
mkdir -p /opt/wordlists
wget -O /opt/wordlists/rockyou.txt https://...
```

### Method 3: Virtual Environment (Development)

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -e ".[dev]"

# Verify
python -c "import red_wifi; print(red_wifi.__version__)"
```

## Configuration

### WiFi Adapter Setup

#### 1. Identify Your Adapter

```bash
# List network interfaces
iwconfig

# Output example:
# wlan0     IEEE 802.11  ESSID:"..."
# eth0      Ethernet     HWaddr 00:11:22:33:44:55
```

#### 2. Enable Monitor Mode

```bash
# Using Red WiFi
red-wifi monitor wlan0

# Or manually
sudo airmon-ng start wlan0
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode Monitor
sudo ifconfig wlan0 up
```

#### 3. Verify Monitor Mode

```bash
iwconfig wlan0
# Should show "Mode:Monitor"
```

### Wordlist Configuration

Red WiFi supports custom wordlists for password cracking:

```bash
# Default location
/opt/wordlists/rockyou.txt

# Popular wordlists
- rockyou.txt (14 million passwords)
- darkweb2017-top10000.txt
- common.txt
- passwords.txt

# Download wordlists
wget -O rockyou.txt https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/Leaked-Databases/rockyou.txt

# Use custom wordlist
red-wifi auto --wordlist /path/to/wordlist.txt
```

## Quick Start

### Step 1: Verify Setup

```bash
# Check Red WiFi installation
red-wifi --version

# Run tests
python3 -m pytest tests/

# Show help
red-wifi --help
```

### Step 2: Scan Networks

```bash
# Enable monitor mode first
red-wifi monitor wlan0

# Scan for 30 seconds
red-wifi scan --interface wlan0 --duration 30

# Example output:
# SSID              BSSID               Encryption
# HomeNetwork       AA:BB:CC:DD:EE:FF   WPA2
# GuestWiFi        11:22:33:44:55:66   WPA2
```

### Step 3: Run Attack

```bash
# Interactive automated attack
red-wifi auto --interface wlan0 --mode aggressive

# Specific target
red-wifi auto --interface wlan0 --target AA:BB:CC:DD:EE:FF

# With custom wordlist
red-wifi auto --interface wlan0 --wordlist /opt/wordlists/rockyou.txt
```

### Step 4: Analyze Results

```bash
# Results are saved in current directory
ls -la
# pentest_report.json
# pentest_report.html
# session.json

# View results
cat pentest_report.json | jq .
```

## Troubleshooting

### Monitor Mode Not Working

**Problem**: "Failed to enable monitor mode"

**Solution**:
```bash
# Check adapter capabilities
sudo airmon-ng check wlan0

# Kill conflicting processes
sudo airmon-ng check kill

# Try again
red-wifi monitor wlan0
```

### No Networks Found

**Problem**: Scan returns 0 networks

**Solution**:
```bash
# Verify monitor mode
iwconfig wlan0
# Should show "Mode:Monitor"

# Check WiFi is working
sudo airodump-ng wlan0

# Try longer scan duration
red-wifi scan --interface wlan0 --duration 60
```

### Permission Denied

**Problem**: "Operation not permitted"

**Solution**:
```bash
# Most operations require root
sudo red-wifi scan --interface wlan0

# Or use sudo for individual commands
sudo python3 -c "from red_wifi import *"
```

### Handshake Capture Fails

**Problem**: "Failed to capture handshake"

**Solution**:
```bash
# 1. Verify target is online
red-wifi scan --interface wlan0

# 2. Get closer to target network
# (Better signal = better capture rate)

# 3. Try longer capture time (default 120s)
# Increase timeout in script or code

# 4. Verify valid handshake
cowpatty -r handshake.cap -c
```

### Cracking Not Working

**Problem**: "Password not found"

**Solution**:
```bash
# 1. Verify handshake is valid
cowpatty -r capture.cap -c
# Should output: "1 handshake(s)"

# 2. Check wordlist
# Password might not be in wordlist
wc -l /opt/wordlists/rockyou.txt

# 3. Try different method
red-wifi crack capture.cap --wordlist rockyou.txt --method john

# 4. Check GPU (if using hashcat)
nvidia-smi  # For NVIDIA
rocm-smi    # For AMD
```

## Next Steps

1. **Read Usage Guide**: See [USAGE.md](USAGE.md)
2. **Learn Attack Modes**: See [ATTACK_MODES.md](ATTACK_MODES.md)
3. **View Examples**: Check `examples/` directory
4. **Read FAQ**: See [FAQ.md](FAQ.md)

## Common Commands

```bash
# Show help for specific command
red-wifi scan --help
red-wifi auto --help
red-wifi crack --help

# List all commands
red-wifi --help

# Show version
red-wifi --version

# Show features
red-wifi features

# Show command reference
red-wifi commands
```

## Getting Help

- **Documentation**: Check [README.md](../README.md)
- **Issues**: Report problems on [GitHub](https://github.com/redwifi/red-wifi/issues)
- **FAQ**: See [FAQ.md](FAQ.md)
- **Discord**: Join community server (link in README)

## Legal Notice

Red WiFi is for **authorized security testing only**. Ensure you have written permission before testing any network.

See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md) for full terms.

---

Ready to start? Run `red-wifi scan --help` to see all options!
