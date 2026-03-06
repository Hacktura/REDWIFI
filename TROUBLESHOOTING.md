# Troubleshooting Guide

Solutions to common Red WiFi problems.

## Installation Issues

### Issue: "Module not found" when importing

**Error**:
```
ModuleNotFoundError: No module named 'red_wifi'
```

**Solution**:
```bash
# Install from source
cd red-wifi
pip3 install -e .

# Or install from PyPI
pip3 install red-wifi

# Verify
python3 -c "import red_wifi; print(red_wifi.__version__)"
```

### Issue: "Permission denied" on setup.sh

**Error**:
```
bash: setup.sh: Permission denied
```

**Solution**:
```bash
# Make executable and run as root
sudo bash setup.sh

# Or
chmod +x setup.sh
sudo ./setup.sh
```

### Issue: Python 3 not found

**Error**:
```
command not found: python3
```

**Solution**:
```bash
# Install Python
sudo apt-get install python3 python3-pip

# Verify
python3 --version
```

---

## Monitor Mode Issues

### Issue: Monitor mode not working

**Error**:
```
Failed to enable monitor mode
```

**Diagnostic**:
```bash
# Check if interface supports monitor mode
sudo airmon-ng

# Check current mode
iwconfig wlan0
```

**Solution**:
```bash
# Kill conflicting processes
sudo airmon-ng check kill

# Try enabling again
sudo airmon-ng start wlan0
# Or use Red WiFi
red-wifi monitor wlan0

# Verify
iwconfig wlan0
# Should show "Mode:Monitor"
```

### Issue: "Interface not found"

**Error**:
```
Interface wlan0 not found
```

**Solution**:
```bash
# List all interfaces
ifconfig
# Or
iwconfig

# Use the correct name
red-wifi scan --interface [correct_name]
```

### Issue: "No such device"

**Error**:
```
No such device
```

**Solution**:
```bash
# Check adapter is plugged in
lsusb
# Should list your adapter

# Restart adapter
sudo ifconfig wlan0 down
sudo ifconfig wlan0 up

# Or unplug/replug USB adapter
```

---

## Scanning Issues

### Issue: No networks found during scan

**Error**:
```
Found 0 networks
```

**Checklist**:
- [ ] Monitor mode enabled: `iwconfig wlan0` should show "Monitor"
- [ ] Adapter powered on and working
- [ ] WiFi networks actually exist nearby
- [ ] Correct interface specified

**Solution**:
```bash
# 1. Verify monitor mode
iwconfig wlan0

# 2. Try manual scan
sudo airodump-ng wlan0

# 3. Increase scan duration
red-wifi scan --interface wlan0 --duration 60

# 4. Check adapter is detected
lsusb
```

### Issue: Only finds same networks repeatedly

**Error**:
```
Warning: Same SSID detected multiple times
```

**Explanation**:
This can happen if multiple networks use same SSID.

**Solution**:
Networks with same SSID may have different BSSIDs (MAC addresses). This is normal. All will be listed.

---

## Handshake Capture Issues

### Issue: Handshake capture always fails

**Error**:
```
Failed to capture handshake
```

**Solutions**:

1. **Check signal strength**:
   ```bash
   red-wifi scan --interface wlan0
   # Look for RSSI value > -70 (stronger signal better)
   ```

2. **Get closer to target**:
   - Move closer to the WiFi router
   - 10-20 feet is usually good range

3. **Ensure target is online**:
   - Someone must be using the network
   - Devices actively connected better

4. **Increase timeout**:
   ```python
   framework.capture_handshake(bssid, channel, timeout=300)  # 5 minutes
   ```

5. **Try different adapter/channel**:
   ```bash
   red-wifi scan --interface wlan0 --band 2.4
   # Note the channel, might need to try 5GHz
   ```

### Issue: "Handshake invalid" when cracking

**Error**:
```
cowpatty: 0 handshakes found
```

**Solution**:
```bash
# Verify handshake
cowpatty -r capture.cap -c

# If invalid, re-capture:
python3 -c "
from red_wifi import *
framework = WiFiPentestFramework('wlan0')
framework.initialize()
framework.capture_handshake('AA:BB:CC:DD:EE:FF', 6, timeout=120)
"
```

---

## Password Cracking Issues

### Issue: "Password not found" after cracking

**Error**:
```
No password found
```

**Reasons**:
1. Password not in wordlist
2. Invalid handshake
3. Wrong network targeted

**Solutions**:
```bash
# 1. Verify handshake is valid
cowpatty -r capture.cap -c
# Should show "1 handshake(s)"

# 2. Try larger wordlist
red-wifi crack capture.cap -w /opt/wordlists/rockyou-all.txt

# 3. Try different method
red-wifi crack capture.cap -w rockyou.txt --method john

# 4. Verify correct BSSID
tcpdump -r capture.cap | grep SSID
```

### Issue: Cracking is very slow

**Causes**:
- Using CPU instead of GPU
- Small CPU capability
- Large wordlist
- Wrong method

**Solutions**:
```bash
# Use GPU (if available)
nvidia-smi  # Check if NVIDIA GPU

# Use hashcat for GPU
hashcat -m 2500 capture.cap rockyou.txt

# Or use smaller wordlist
head -n 1000000 rockyou.txt > top1m.txt
red-wifi crack capture.cap -w top1m.txt
```

### Issue: Hashcat "No devices found"

**Error**:
```
hashcat: No CUDA devices found
```

**Explanation**:
GPU not detected or not installed.

**Solution**:
- Check NVIDIA GPU: `nvidia-smi`
- Install drivers: `sudo apt-get install nvidia-driver-520`
- Or use CPU method: `--method john`

---

## Permission Issues

### Issue: "Operation not permitted"

**Error**:
```
Operation not permitted: No such device
```

**Solution**:
```bash
# Use sudo
sudo red-wifi scan --interface wlan0

# Or enable monitor mode with sudo
sudo red-wifi monitor wlan0
```

### Issue: "Cannot open device"

**Error**:
```
Cannot open device for rx packets: Permission denied
```

**Solution**:
```bash
# Run as root
sudo red-wifi scan --interface wlan0

# Or add user to dialout group
sudo usermod -a -G dialout $USER
# Then logout and login again
```

---

## Software Dependency Issues

### Issue: "aircrack-ng not found"

**Error**:
```
FileNotFoundError: aircrack-ng command not found
```

**Solution**:
```bash
sudo apt-get install aircrack-ng

# Verify
aircrack-ng --version
```

### Issue: "hashcat not installed"

**Error**:
```
FileNotFoundError: hashcat
```

**Solution**:
```bash
sudo apt-get install hashcat

# Verify
hashcat --version
```

### Issue: "john not found"

**Error**:
```
FileNotFoundError: john
```

**Solution**:
```bash
sudo apt-get install john

# Verify
john --version
```

---

## Adapter Issues

### Issue: Adapter keeps disconnecting

**Error**:
```
Adapter unavailable
Lost connection
```

**Solutions**:
```bash
# Check adapter temperature (might be overheating)
lsusb

# Try different USB port
# Or use powered USB hub

# Update drivers
sudo apt-get install firmware-ralink
```

### Issue: "Bad CRC checksum"

**Error**:
```
Bad CRC or plcp error: ...
```

**Explanation**:
Network interference or weak signal.

**Solution**:
- Move away from interference sources
- Use different channel
- Get closer to target

---

## Performance Issues

### Issue: System becomes slow during scan

**Cause**:
High CPU/memory usage.

**Solution**:
```bash
# Monitor usage
htop

# Run with lower priority
nice -n 19 red-wifi scan --interface wlan0

# Reduce scan duration
red-wifi scan --interface wlan0 --duration 30
```

---

## File Issues

### Issue: "File not found" for wordlist

**Error**:
```
FileNotFoundError: rockyou.txt
```

**Solution**:
```bash
# Verify wordlist exists
ls -la /opt/wordlists/rockyou.txt

# Use absolute path
red-wifi crack capture.cap -w /opt/wordlists/rockyou.txt

# Or download
wget -O rockyou.txt https://...
```

### Issue: "Permission denied" for capture file

**Error**:
```
PermissionError: capture.cap
```

**Solution**:
```bash
# Check permissions
ls -la capture.cap

# Make readable
chmod 644 capture.cap

# Or sudo
sudo red-wifi crack capture.cap -w rockyou.txt
```

---

## Windows/macOS Issues

### Using Windows?

Red WiFi is designed for Linux. For Windows:

Option 1: **WSL2** (Windows Subsystem for Linux)
```bash
# Install WSL2
# Then install Red WiFi in Linux subsystem
```

Option 2: **Virtual Machine**
```bash
# Use VirtualBox with Ubuntu
# Install Red WiFi in guest OS
```

Option 3: **Kali on USB**
```bash
# Boot live Kali Linux from USB
# Install and run Red WiFi
```

### Using macOS?

Limited support (aircrack-ng works on macOS):

```bash
# Install homebrew first
/bin/bash -c "$(curl -fsSL ...)"

# Install dependencies
brew install python3 aircrack-ng hashcat

# Install Red WiFi
pip3 install red-wifi
```

---

## Getting More Help

- Check [FAQ.md](FAQ.md) for common questions
- Review [USAGE.md](USAGE.md) for proper command syntax
- Check [ATTACK_MODES.md](ATTACK_MODES.md) for mode details
- Open issue on GitHub with full error output

---

## Diagnostic Steps

Run this for diagnostics:

```bash
echo "=== System Info ==="
uname -a
python3 --version

echo "=== Adapter Check ==="
iwconfig
lsusb

echo "=== Tool Check ==="
aircrack-ng --version
hashcat --version
john --version

echo "=== Red WiFi Check ==="
python3 -c "import red_wifi; print(red_wifi.__version__)"
red-wifi --version
```

Provide this output when reporting issues.

---

Last updated: January 2024
