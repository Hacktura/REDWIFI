"""
Red WiFi Example: Basic Network Scanning
Demonstrates how to scan for available WiFi networks.
"""

from red_wifi import WiFiPentestFramework
from red_wifi.advanced_attacks import EncryptionAnalyzer


def main():
    """Run basic network scan."""
    
    # Initialize framework
    print("Initializing Red WiFi Framework...")
    framework = WiFiPentestFramework("wlan0")  # Replace with your interface
    
    if not framework.initialize():
        print("Failed to initialize framework")
        return
    
    # Perform network scan
    print("\nScanning for networks (30 seconds)...")
    networks = framework.scan_networks(duration=30)
    
    # Analyze encryption security
    analyzer = EncryptionAnalyzer(framework.logger)
    analysis = analyzer.analyze_network_security(networks)
    
    # Display results
    print(f"\n{'SSID':<30} {'BSSID':<20} {'Channel':<10} {'Encryption':<15}")
    print("-" * 75)
    
    for net in networks:
        print(f"{net.ssid:<30} {net.bssid:<20} {net.channel:<10} {net.encryption:<15}")
    
    # Show security assessment
    print(f"\n{'SECURITY ANALYSIS':<50}")
    print("-" * 50)
    print(f"Total Networks: {analysis['total_networks']}")
    print(f"Critical: {analysis['critical_networks']}")
    print(f"High Risk: {analysis['high_risk_networks']}")
    print(f"Medium Risk: {analysis['medium_risk_networks']}")
    print(f"Secure: {analysis['secure_networks']}")
    
    # Save session
    print("\nSaving session...")
    framework.session_data['scan_results'] = networks
    framework.save_session("basic_scan_session.json")
    
    print("Scan complete!")


if __name__ == "__main__":
    main()
