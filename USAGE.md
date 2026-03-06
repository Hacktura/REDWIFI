# Red WiFi Usage Guide

Complete guide to using Red WiFi for WiFi penetration testing.

## Command-Line Interface

### Scan Command

Scan for available WiFi networks.

```bash
red-wifi scan --interface wlan0 [OPTIONS]
```

**Options**:
- `--interface, -i` (required): Network interface (e.g., wlan0)
- `--duration, -d`: Scan duration in seconds (default: 30)
- `--band, -b`: Frequency band (2.4, 5, all) (default: all)

**Examples**:
```bash
# Basic scan
red-wifi scan --interface wlan0

# 2.4GHz only, 60 seconds
red-wifi scan -i wlan0 -b 2.4 -d 60

# 5GHz only
red-wifi scan -i wlan0 --band 5
```

### Auto Attack Command

Launch automated WiFi attacks.

```bash
red-wifi auto --interface wlan0 [OPTIONS]
```

**Options**:
- `--interface, -i` (required): Network interface
- `--mode, -m`: Attack mode (passive, aggressive, relentless, stealth)
- `--target, -t`: Target BSSID (optional)
- `--wordlist, -w`: Password wordlist
- `--strategy, -s`: Attack strategy (wpa, wps, hybrid, all)

**Examples**:
```bash
# Interactive attack menu
red-wifi auto --interface wlan0

# Aggressive mode
red-wifi auto -i wlan0 --mode aggressive

# Specific target
red-wifi auto -i wlan0 --target AA:BB:CC:DD:EE:FF

# Custom wordlist
red-wifi auto -i wlan0 -w /path/to/wordlist.txt

# WPS only
red-wifi auto -i wlan0 --strategy wps
```

### Crack Command

Crack captured WPA handshake.

```bash
red-wifi crack <handshake.cap> --wordlist <wordlist.txt> [OPTIONS]
```

**Options**:
- `<handshake.cap>` (required): Capture file
- `--wordlist, -w` (required): Password wordlist
- `--method, -m`: Cracking method (hashcat, john) (default: hashcat)

**Examples**:
```bash
# Basic cracking
red-wifi crack capture.cap --wordlist rockyou.txt

# Using John
red-wifi crack capture.cap -w wordlist.txt --method john

# Relative path
red-wifi crack ./captures/network.cap -w /opt/wordlists/rockyou.txt
```

### Monitor Mode Commands

Enable/disable monitor mode on WiFi adapter.

```bash
# Enable monitor mode
red-wifi monitor wlan0

# Disable monitor mode
red-wifi managed wlan0
```

## Python API

### Basic Usage

```python
from red_wifi import WiFiPentestFramework

# Initialize framework
framework = WiFiPentestFramework("wlan0")
if not framework.initialize():
    exit(1)

# Scan networks
networks = framework.scan_networks(duration=30)

# Print results
for net in networks:
    print(f"{net.ssid}: {net.encryption} ({net.rssi}dBm)")
```

### Network Scanning

```python
# Scan specific band
from red_wifi import NetworkScanner

scanner = NetworkScanner(framework.logger, "wlan0")

# Scan 2.4GHz
networks_2ghz = scanner.scan_24ghz(duration=30)

# Scan 5GHz
networks_5ghz = scanner.scan_5ghz(duration=30)

# Scan all bands
all_networks = scanner.scan_all(duration=30)
```

### Handshake Capture

```python
from red_wifi import HandshakeCapturer

capturer = HandshakeCapturer(framework.logger, "wlan0")

# Capture handshake
success = capturer.capture_handshake(
    bssid="AA:BB:CC:DD:EE:FF",
    channel=6,
    output="capture.cap",
    timeout=120
)

if success:
    print("Handshake captured!")
```

### Password Cracking

```python
from red_wifi import PasswordCracker

cracker = PasswordCracker(framework.logger)

# Dictionary attack
password = cracker.crack_with_wordlist(
    "capture.cap",
    "rockyou.txt",
    method="hashcat"
)

if password:
    print(f"Password found: {password}")
```

### Automated Attacks

```python
from red_wifi import AutomatedAttacker, AttackMode, AttackStrategy

# Initialize attacker
attacker = AutomatedAttacker(framework)

# Rank targets
ranked = attacker.rank_targets(networks)

# Execute attack
result = attacker.attack(
    target=networks[0],
    mode=AttackMode.AGGRESSIVE,
    strategy=AttackStrategy.HYBRID,
    wordlist="rockyou.txt"
)

print(f"Success: {result.success}")
print(f"Password: {result.password}")
print(f"Duration: {result.duration}s")
```

### Security Analysis

```python
from red_wifi import EncryptionAnalyzer

analyzer = EncryptionAnalyzer(framework.logger)

# Analyze single network
assessment = analyzer.assess_vulnerability(networks[0])
print(assessment["vulnerability_level"])

# Analyze all networks
analysis = analyzer.analyze_network_security(networks)
print(f"Critical: {analysis['critical_networks']}")
print(f"High Risk: {analysis['high_risk_networks']}")
```

### Reporting

```python
# Generate JSON report
framework.reporter.generate_json_report(
    framework.session_data,
    "report.json"
)

# Generate HTML report
framework.reporter.generate_html_report(
    framework.session_data,
    "report.html"
)

# Save session
framework.save_session("session.json")

# Load session
framework.load_session("session.json")
```

## Attack Workflows

### Complete Attack Workflow

```python
from red_wifi import *

# 1. Initialize
framework = WiFiPentestFramework("wlan0")
framework.initialize()

# 2. Scan
networks = framework.scan_networks(30)
print(f"Found {len(networks)} networks")

# 3. Select target
target = networks[0]
print(f"Target: {target.ssid}")

# 4. Capture handshake
framework.capture_handshake(target.bssid, target.channel)

# 5. Crack password
password = framework.crack_password("capture.cap", "rockyou.txt")

# 6. Generate report
framework.session_data['target'] = target.ssid
framework.session_data['password'] = password
framework.generate_report("json")

# 7. Save session
framework.save_session()
```

### Multi-Target Attack

```python
from red_wifi import *

framework = WiFiPentestFramework("wlan0")
framework.initialize()

networks = framework.scan_networks()
attacker = AutomatedAttacker(framework)

# Rank and select top targets
ranked = attacker.rank_targets(networks)
targets = [net for net, _ in ranked[:5]]

# Attack all targets
results = attacker.multi_target_attack(
    targets,
    mode=AttackMode.AGGRESSIVE,
    wordlist="rockyou.txt"
)

# Print results
for result in results:
    status = "✓" if result.success else "✗"
    print(f"{status} {result.target.ssid}")
    if result.password:
        print(f"  Password: {result.password}")
```

### Advanced Analysis

```python
from red_wifi import *

analyzer = EncryptionAnalyzer(framework.logger)
wpa_attacks = AdvancedWPAAttacks(framework.logger)

# Analyze all networks
analysis = analyzer.analyze_network_security(networks)

# Examine vulnerabilities
for net_analysis in analysis['networks']:
    if net_analysis['vulnerability_level'] == 'CRITICAL':
        print(f"CRITICAL: {net_analysis['network']}")
        print(f"Exploitability: {net_analysis['exploitability']}")

# PMKID attack
pmkid = wpa_attacks.pmkid_attack(target.bssid, "wlan0")
if pmkid:
    print("PMKID found!")
```

## Configuration Files

### Session Management

Red WiFi saves sessions automatically:

```python
# Auto-saved session data
framework.session_data = {
    'scan_results': [...],
    'targets': [...],
    'attack_results': [...],
    'passwords_found': [...]
}

# Save to file
framework.save_session("my_session.json")

# Load from file
framework.load_session("my_session.json")
```

### Wordlist Configuration

```python
# Use default
red-wifi auto -i wlan0

# Use custom wordlist
red-wifi auto -i wlan0 -w /path/to/custom.txt

# Use multiple wordlists
for wordlist in wordlists/*.txt:
    red-wifi crack capture.cap -w $wordlist
```

## Logging and Output

### Console Output

Red WiFi uses color-coded output:
- `[*]` - Information (cyan)
- `[+]` - Success (green)
- `[!]` - Error (red)
- `[⚠]` - Warning (yellow)

### Log Files

Logs are saved in `logs/` directory:

```bash
ls logs/
# RedWiFi_20240101_120000.log
# RedWiFi_20240101_130000.log
```

### Verbose Output

```python
# Enable debug logging
framework.logger.debug("Debug message")
framework.logger.info("Info message")
framework.logger.error("Error message")
```

## Performance Tips

1. **Faster Cracking**: Use aggressive mode with GPU
2. **Better Handshakes**: Position close to target
3. **Longer Scans**: Use 60+ seconds for complete coverage
4. **Large Wordlists**: Optimize with rules instead
5. **Multiple Interfaces**: Attack multiple targets simultaneously

