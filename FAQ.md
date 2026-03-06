# Frequently Asked Questions

## General Questions

**Q: Is Red WiFi legal to use?**  
A: Red WiFi is a tool for authorized security testing only. You must have written permission from the network owner. Using it on networks you don't own is illegal in most jurisdictions. See CODE_OF_CONDUCT.md.

**Q: What's the success rate?**  
A: Success depends on many factors:
- Password strength
- Wordlist size
- Encryption type
- WiFi signal strength
- Typically 70-95% for WPA2 with good wordlists

**Q: Can I crack WPA3?**  
A: WPA3 is significantly more secure than WPA2. Red WiFi supports testing but cracking is much harder. Unlikely with dictionary attack.

**Q: Do I need admin/root access?**  
A: Yes, monitor mode and packet injection require root/sudo privileges.

**Q: Can I use this on Raspberry Pi?**  
A: Yes, if you have a compatible WiFi adapter, but speed will be slower.

---

## Installation Questions

**Q: I get "Module not found" error**  
A: Run `pip3 install -r requirements.txt` then `pip3 install -e .`

**Q: Monitor mode not working**  
A: Your adapter may not support monitor mode. Check:
```bash
sudo airmon-ng
```

**Q: Setup script fails with permission error**  
A: The setup script requires root. Run: `sudo bash setup.sh`

**Q: How do I uninstall Red WiFi?**  
A: Run: `pip3 uninstall red-wifi`

---

## Usage Questions

**Q: What's the difference between attack modes?**  
A: See ATTACK_MODES.md. In short:
- Passive: Stealthy but slow
- Aggressive: Balanced (recommended)
- Relentless: Fast but obvious
- Stealth: Moderate speed, zero detection

**Q: How long does password cracking take?**  
A: Depends on:
- Password length (14 char: hours to days)
- Password complexity
- Wordlist size
- Hardware (GPU much faster)

**Q: Can I attack multiple targets at once?**  
A: Yes, using multi_target_attack() in Python API.

**Q: What wordlist should I use?**  
A: Download rockyou.txt (14 million passwords):
```bash
wget https://raw.githubusercontent.com/[...]/rockyou.txt
```

**Q: How do I know if scan found networks?**  
A: Check output:
```bash
red-wifi scan --interface wlan0
# Found 12 networks
```

---

## Technical Questions

**Q: What's a handshake and why is it important?**  
A: A handshake is the authentication exchange. You need it to crack the password offline.

**Q: What's the difference between WPA and WPA2?**  
A: WPA2 is newer and more secure. Both are vulnerable to dictionary attacks.

**Q: What's WPS and why disable it?**  
A: WPS allows quick connection but is vulnerable to PIN bruteforce. Disable in router settings.

**Q: What's monitor mode?**  
A: Special mode where WiFi adapter captures all packets without joining network.

**Q: Why is GPU cracking faster?**  
A: GPUs can test millions of passwords/second. CPUs are much slower.

---

## Troubleshooting Questions

**Q: "No networks found" even though I see WiFi**  
A: 
- Verify monitor mode: `iwconfig wlan0`
- Increase scan time: `--duration 60`
- Try different adapter

**Q: Handshake capture always fails**  
A:
- Get closer to target
- Verify adapter range
- Try longer timeout
- Check target is online

**Q: Password cracking finds nothing**  
A:
- Password not in wordlist
- Handshake is invalid (verify with cowpatty)
- Try different wordlist

**Q: "Permission denied" errors**  
A: Use sudo: `sudo red-wifi scan --interface wlan0`

**Q: "Interface not found"**  
A: Check interface name: `iwconfig` then use correct name.

---

## Performance Questions

**Q: How can I make attacks faster?**  
A:
- Use Relentless mode (faster but obvious)
- Use GPU for cracking
- Use smaller, optimized wordlist
- Position close to target

**Q: Can I run multiple attacks simultaneously?**  
A: Yes, from Python API with multiple instances.

**Q: How much RAM does Red WiFi use?**  
A: Minimal (~50MB) plus whatever hashcat uses (varies).

---

## Results Questions

**Q: Where are results saved?**  
A: Current directory by default:
```
pentest_report.json
pentest_report.html
session.json
```

**Q: How do I save results for a client?**  
A: Reports are generated automatically as HTML and JSON.

**Q: Can I schedule automated scans?**  
A: Use cron jobs:
```bash
0 2 * * * red-wifi auto --interface wlan0 >> /tmp/wifi_scan.log
```

---

## Compatibility Questions

**Q: Which WiFi adapters work best?**  
A: Recommended:
- Alfa AWUS036ACH (best)
- TP-Link TL-WN722N (budget)
- Netgear WNDA3100

**Q: Does it work on macOS?**  
A: Not officially (aircrack-ng support is limited).

**Q: Does it work on Windows?**  
A: Not directly. Use WSL2 or virtual machine.

**Q: What Linux distributions are supported?**  
A: Any with aircrack-ng support. Kali and Ubuntu tested.

---

## Advanced Questions

**Q: Can I write custom attack modules?**  
A: Yes, extend the framework classes in Python.

**Q: Can I integrate with other tools?**  
A: Yes, Red WiFi generates standard outputs (PCAP files, JSON).

**Q: How do I contribute to Red WiFi?**  
A: See CONTRIBUTING.md on GitHub.

**Q: Is there a commercial version?**  
A: Currently open-source MIT licensed.

---

## Security Questions

**Q: Is Red WiFi safe to use?**  
A: Yes, if used only on authorized networks. See CODE_OF_CONDUCT.md.

**Q: Does it send data to external servers?**  
A: No, everything is local. No cloud connectivity.

**Q: Can I use it in restricted environments?**  
A: Only with explicit authorization. Check employer/school policies.

---

## Support Questions

**Q: How do I report a bug?**  
A: Open an issue on GitHub with:
- Detailed description
- Steps to reproduce
- Error output
- Your environment (OS, Python version)

**Q: How do I request a feature?**  
A: Open a feature request on GitHub.

**Q: Is there a Discord/Slack community?**  
A: Check README.md for community links.

---

## More Help

- **Documentation**: Check docs/ folder
- **Examples**: See examples/ folder
- **GitHub Issues**: Report problems there
- **Troubleshooting Guide**: See TROUBLESHOOTING.md

---

Last updated: January 2024
