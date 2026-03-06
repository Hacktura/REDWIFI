# Changelog

All notable changes to Red WiFi are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-15

### Added
- Complete WiFi penetration testing framework
- Multiple attack modes: Passive, Aggressive, Relentless, Stealth
- Automated target selection and ranking
- WPA/WPA2/WPA3 handshake capture
- Dictionary, rule-based, and hybrid cracking methods
- WPS vulnerability testing (Pixie Dust, PIN bruteforce)
- PMKID attack support
- Client-side attacks (deauth, evil twin detection)
- Advanced encryption analysis
- Professional JSON/HTML reporting
- Session management and persistence
- Interactive CLI menu
- Comprehensive documentation
- Full test suite
- GitHub Actions CI/CD

### Core Features
- **Network Scanning**: 2.4GHz and 5GHz band detection
- **Encryption Analysis**: WEP, WPA, WPA2, WPA3 classification
- **Attack Automation**: One-command assault orchestration
- **Cracking**: GPU and CPU acceleration support
- **Reporting**: Professional vulnerability assessments

### Documentation
- Getting started guide
- Detailed usage documentation
- Complete API reference
- 100+ command examples
- Troubleshooting guide
- FAQ section

### Testing
- Comprehensive import tests
- Module verification
- Basic functionality tests
- Example scripts

## [1.0.0] - 2023-12-01

### Added
- Initial release
- Basic network scanning
- Simple WPA cracking
- Handshake capture
- Basic reporting

### Known Limitations
- Limited to aircrack-ng suite
- No WPS support
- Manual target selection
- Basic reporting only

## Future Roadmap

### Planned for v2.1.0
- KRACK attack implementation
- Beacon spoofing
- Rogue AP framework
- Enhanced PMKID support
- Multi-interface support
- Wireless IDS integration

### Planned for v2.2.0
- Machine learning target ranking
- Advanced frame analysis
- Packet manipulation tools
- Custom attack chains
- Integration with other tools (Metasploit, Burp)

### Planned for v3.0.0
- Full WiFi 6 (802.11ax) support
- Distributed attack coordination
- Cloud-based reporting
- Mobile app companion
- Enterprise deployment features

## Version Support

| Version | Status | Release Date | End of Support |
|---------|--------|-------------|-----------------|
| 2.0.0 | Current | 2024-01-15 | 2025-01-15 |
| 1.0.0 | Deprecated | 2023-12-01 | 2024-01-15 |

## Security Updates

Critical security updates will be released as needed. Please keep Red WiFi updated.

## Upgrade Path

- **From 1.0.0 to 2.0.0**: Breaking changes. See upgrade guide in docs.
- **Between 2.x versions**: Backward compatible unless noted.

## Contributors

### Active Contributors
- Red WiFi Core Team
- Community contributors

### Special Thanks
To the open-source security research community.

## License

Red WiFi is licensed under the MIT License. See LICENSE file for details.

---

**Note**: This changelog covers Red WiFi versions only. For tool-specific changes (aircrack-ng, hashcat, etc.), see their respective projects.
