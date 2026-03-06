# Red WiFi v2.0

<div align="center">

![Red WiFi Logo](https://img.shields.io/badge/Red%20WiFi-2.0.0-red?style=flat-square&logo=wifi)
![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)

**Professional WiFi Penetration Testing Framework**

[Documentation](#documentation) • [Features](#features) • [Installation](#installation) • [Quick Start](#quick-start) • [Examples](#examples)

</div>

---

## Overview

Red WiFi is a professional-grade WiFi penetration testing framework designed for security researchers, penetration testers, and authorized security professionals. It automates the full WiFi attack workflow with multiple attack modes, intelligent target selection, and professional reporting.

### Key Highlights

- **🚀 Automated Attacks** - One-command WiFi penetration testing
- **🎯 Smart Targeting** - AI-powered target ranking and selection
- **🔒 Multi-Method Cracking** - Dictionary, rule-based, hybrid, GPU-accelerated
- **⚡ Multiple Modes** - Passive, Aggressive, Relentless, Stealth
- **📊 Professional Reports** - JSON and HTML vulnerability assessments
- **🛡️ Advanced Analysis** - Encryption strength, WPS vulnerabilities, client threats
- **🔧 Modular Architecture** - Extensible for custom implementations

---

## Features Matrix

### Attack Capabilities

| Feature | Status | Details |
|---------|--------|---------|
| Network Scanning | ✓ | 2.4GHz & 5GHz multi-band |
| WPA/WPA2/WPA3 | ✓ | All modern encryption standards |
| Handshake Capture | ✓ | Full 4-way handshake extraction |
| Dictionary Attacks | ✓ | Wordlist-based cracking |
| Rule-Based Attacks | ✓ | Pattern generation and testing |
| Hybrid Attacks | ✓ | Combined wordlist + mask |
| GPU Acceleration | ✓ | Hashcat integration |
| WPS Testing | ✓ | Pixie Dust & PIN bruteforce |
| Client Attacks | ✓ | Deauth, evil twin, fragmentation |
| PMKID Attacks | ✓ | Fast RSN IE extraction |

### Attack Modes

```
Passive   (10-30 min)   → Undetectable listen-only
Aggressive (2-5 min)    → Standard active deauth
Relentless (1-2 min)    → Maximum aggression flooding
Stealth (20-30 min)     → Zero-detection low-power
```

### Analysis Features

- Encryption vulnerability assessment
- WPS vulnerability detection
- Signal strength analysis
- Client enumeration
- Evil twin detection
- Network security ranking
- Detailed vulnerability reports

---

## Installation

### Prerequisites

- Linux (Ubuntu/Kali recommended)
- Python 3.8 or higher
- WiFi adapter with monitor mode support
- Root/sudo access

### Quick Install

```bash
# Clone repository
git clone https://github.com/redwifi/red-wifi.git
cd red-wifi

# Run setup script (installs all dependencies)
sudo bash setup.sh

# Or install manually
sudo apt-get update
sudo apt-get install -y aircrack-ng hashcat john
pip3 install -r requirements.txt
pip3 install -e .
```

### Verify Installation

```bash
# Check import
python3 -c "import red_wifi; print(f'Red WiFi {red_wifi.__version__} installed')"

# Run tests
python3 -m pytest tests/

# Show help
red-wifi --help
```

---

## Quick Start

### 1. Enable Monitor Mode

```bash
red-wifi monitor wlan0
```

### 2. Scan Networks

```bash
red-wifi scan --interface wlan0 --duration 30
```

### 3. Launch Automated Attack

```bash
red-wifi auto --interface wlan0 --mode aggressive
```

### 4. Crack Handshake

```bash
red-wifi crack handshake.cap --wordlist rockyou.txt
```

---

## Usage Examples

### Basic Network Scanning

```python
from red_wifi import WiFiPentestFramework
from red_wifi.advanced_attacks import EncryptionAnalyzer

# Initialize framework
framework = WiFiPentestFramework("wlan0")
framework.initialize()

# Scan networks
networks = framework.scan_networks(duration=30)

# Analyze security
analyzer = EncryptionAnalyzer(framework.logger)
analysis = analyzer.analyze_network_security(networks)

# Display results
for network in networks:
    print(f"{network.ssid}: {network.encryption}")
```

### Automated Attack

```python
from red_wifi import WiFiPentestFramework, AutomatedAttacker, AttackMode

# Initialize
framework = WiFiPentestFramework("wlan0")
framework.initialize()

# Scan and attack
networks = framework.scan_networks()
attacker = AutomatedAttacker(framework)

# Rank targets
ranked = attacker.rank_targets(networks)
targets = [net for net, _ in ranked[:3]]

# Execute attacks
results = attacker.multi_target_attack(
    targets,
    mode=AttackMode.AGGRESSIVE,
    wordlist="rockyou.txt"
)

# Print results
for result in results:
    if result.success:
        print(f"✓ {result.target.ssid}: {result.password}")
```

### Advanced Analysis

```python
from red_wifi import EncryptionAnalyzer, AdvancedWPAAttacks
from red_wifi.advanced_attacks import VulnerabilityReportGenerator

# Create analyzer
analyzer = EncryptionAnalyzer(logger)
assessment = analyzer.analyze_network_security(networks)

# Advanced attacks
wpa_attacks = AdvancedWPAAttacks(logger)
pmkid = wpa_attacks.pmkid_attack("aa:bb:cc:dd:ee:ff", "wlan0")

# Generate report
reporter = VulnerabilityReportGenerator(logger)
reporter.generate_vulnerability_report(assessment)
```

---

## Documentation

### Getting Started
- [Installation Guide](docs/GETTING_STARTED.md)
- [Quick Start Tutorial](docs/GETTING_STARTED.md#quick-start)
- [System Requirements](docs/GETTING_STARTED.md#requirements)

### Usage Guides
- [Complete Usage Guide](docs/USAGE.md)
- [Wifite-Style Automation](docs/WIFITE_GUIDE.md)
- [Attack Modes Explained](docs/ATTACK_MODES.md)
- [Command Reference](QUICK_REFERENCE.sh)

### Advanced Topics
- [API Reference](docs/API.md)
- [Architecture Overview](docs/ARCHITECTURE.md)
- [Custom Attacks](docs/CUSTOM_ATTACKS.md)

### Support
- [Frequently Asked Questions](docs/FAQ.md)
- [Troubleshooting Guide](docs/TROUBLESHOOTING.md)
- [Common Issues](docs/TROUBLESHOOTING.md#common-issues)

---

## Command Reference

```bash
# Scanning
red-wifi scan --interface wlan0 --duration 30
red-wifi scan -i wlan0 --band 2.4

# Automated attacks
red-wifi auto --interface wlan0 --mode aggressive
red-wifi auto -i wlan0 -t AA:BB:CC:DD:EE:FF --wordlist rockyou.txt

# Password cracking
red-wifi crack handshake.cap --wordlist rockyou.txt --method hashcat
red-wifi crack handshake.cap -w wordlist.txt -m john

# Interface management
red-wifi monitor wlan0           # Enable monitor mode
red-wifi managed wlan0           # Disable monitor mode

# Help and info
red-wifi --help
red-wifi features                # Show features
red-wifi commands                # Show command reference
red-wifi --version              # Show version
```

---

## Architecture

### Core Modules

```
red_wifi/
├── wifi_pentest.py        # Core framework & orchestration
├── wifite_integration.py   # Automated attack system
├── advanced_attacks.py     # Advanced exploitation techniques
├── branding.py            # UI & formatting
└── cli.py                 # Command-line interface
```

### Key Classes

- **WiFiPentestFramework** - Main orchestrator
- **NetworkScanner** - Network discovery
- **HandshakeCapturer** - Handshake extraction
- **PasswordCracker** - Cracking methods
- **AutomatedAttacker** - Attack automation
- **EncryptionAnalyzer** - Vulnerability assessment
- **ReportGenerator** - Professional reports

---

## Security & Ethics

### IMPORTANT DISCLAIMER

Red WiFi is designed for **authorized security testing only**:

- ✓ Authorized penetration testing
- ✓ Security research in lab environments
- ✓ Educational use under supervision
- ✗ Unauthorized network testing
- ✗ Illegal network access
- ✗ Criminal hacking activities

**Users are responsible for:**
- Obtaining written authorization before testing
- Complying with all applicable laws
- Following responsible disclosure practices
- Using only on networks they own or have permission to test

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for full terms.

---

## System Requirements

### Operating System
- Ubuntu 18.04 LTS or newer
- Kali Linux 2021+
- Debian 10+
- Other Linux distributions (Ubuntu-based preferred)

### Hardware
- Any computer with a compatible WiFi adapter
- Monitor mode support required
- Minimum 2GB RAM
- Recommended: 4GB+ RAM, fast processor for cracking

### Compatible WiFi Adapters
- Alfa AWUS036ACH
- TP-Link TL-WN722N
- Netgear A6210
- Ralink chipsets
- Atheros chipsets
- Most adapters that support aircrack-ng

### Python
- Python 3.8 - 3.11
- pip3 package manager
- Virtual environment support (recommended)

---

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_imports.py -v

# Run with coverage
pytest tests/ --cov=red_wifi --cov-report=html
```

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
git clone https://github.com/redwifi/red-wifi.git
cd red-wifi
pip install -e ".[dev]"
```

### Code Quality

```bash
# Format code
black red_wifi/ examples/ tests/

# Lint code
flake8 red_wifi/ --max-line-length=127

# Type checking
mypy red_wifi/

# Security scan
bandit -r red_wifi/
```

---

## Troubleshooting

### Monitor Mode Issues
```bash
# Check interface
sudo iwconfig

# Enable monitor mode manually
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode Monitor
sudo ifconfig wlan0 up
```

### Cracking Not Working
- Verify handshake is valid: `cowpatty -r capture.cap -c`
- Check wordlist exists and is readable
- Try different cracking method (hashcat vs john)
- Check for GPU support: `nvidia-smi` (for hashcat)

### Permission Denied Errors
```bash
# Many operations require root
sudo red-wifi scan --interface wlan0
```

---

## Performance Tips

1. **For Speed**: Use Aggressive mode with hashcat GPU acceleration
2. **For Stealth**: Use Stealth mode with patient approach
3. **For Reliability**: Use Passive mode, wait longer
4. **For Cracking**: Use large, optimized wordlists
5. **For Scanning**: Use appropriate duration (30-60 seconds)

---

## FAQ

**Q: Is this legal to use?**  
A: Only on networks you own or have written permission to test. See security note above.

**Q: What's the success rate?**  
A: Depends on password strength, dictionary size, and encryption. Most WPA2 networks crack with appropriate wordlist.

**Q: Can it crack WPA3?**  
A: WPA3 is significantly more secure. Red WiFi supports testing but cracking is much more difficult.

**Q: How long does cracking take?**  
A: Varies from minutes to days depending on password complexity, wordlist size, and hardware.

For more FAQs, see [FAQ.md](docs/FAQ.md)

---

## License

Red WiFi is licensed under the MIT License. See [LICENSE](LICENSE) file for details.

---

## Support

- 📖 [Documentation](docs/)
- 🐛 [Report Issues](https://github.com/redwifi/red-wifi/issues)
- 💬 [Discussions](https://github.com/redwifi/red-wifi/discussions)
- 📧 [Contact](mailto:contact@redwifi.dev)

---

## Acknowledgments

Red WiFi builds on the excellent work of:
- aircrack-ng team
- hashcat developers
- John the Ripper contributors
- The open-source security community

---

## Status

![Tests](https://github.com/redwifi/red-wifi/workflows/Tests/badge.svg)
![Security](https://github.com/redwifi/red-wifi/workflows/Security/badge.svg)

**Version**: 2.0.0  
**Status**: Production Ready  
**Last Updated**: January 2024

---

<div align="center">

**🔴 Red WiFi - Professional WiFi Penetration Testing 🔴**

[⬆ back to top](#red-wifi-v20)

</div>
