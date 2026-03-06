"""
Red WiFi CLI Entry Point
Command-line interface for the Red WiFi framework.
"""

import sys
import argparse
from typing import Optional

from .wifi_pentest import WiFiPentestFramework
from .wifite_integration import AutomatedAttacker, WifiteInteractiveMenu, AttackMode, AttackStrategy
from .advanced_attacks import EncryptionAnalyzer
from .branding import print_banner, print_logo_large, print_quick_commands, print_features_matrix


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser."""
    parser = argparse.ArgumentParser(
        prog='red-wifi',
        description='Red WiFi - Professional WiFi Penetration Testing Framework',
        epilog='Use red-wifi COMMAND --help for command-specific help'
    )
    
    parser.add_argument('--version', action='version', version='Red WiFi v2.0.0')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Scan command
    scan_parser = subparsers.add_parser('scan', help='Scan for WiFi networks')
    scan_parser.add_argument('--interface', '-i', required=True, help='Network interface')
    scan_parser.add_argument('--duration', '-d', type=int, default=30, help='Scan duration (seconds)')
    scan_parser.add_argument('--band', '-b', choices=['2.4', '5', 'all'], default='all', help='Frequency band')
    
    # Auto attack command
    auto_parser = subparsers.add_parser('auto', help='Automated attack mode')
    auto_parser.add_argument('--interface', '-i', required=True, help='Network interface')
    auto_parser.add_argument('--mode', '-m', choices=['passive', 'aggressive', 'relentless', 'stealth'],
                            default='aggressive', help='Attack mode')
    auto_parser.add_argument('--target', '-t', help='Target BSSID')
    auto_parser.add_argument('--wordlist', '-w', help='Password wordlist')
    auto_parser.add_argument('--strategy', '-s', choices=['wpa', 'wps', 'hybrid', 'all'],
                            default='hybrid', help='Attack strategy')
    
    # Crack command
    crack_parser = subparsers.add_parser('crack', help='Crack captured handshake')
    crack_parser.add_argument('handshake', help='Handshake capture file')
    crack_parser.add_argument('--wordlist', '-w', required=True, help='Password wordlist')
    crack_parser.add_argument('--method', '-m', choices=['hashcat', 'john'], default='hashcat')
    
    # Monitor mode commands
    monitor_parser = subparsers.add_parser('monitor', help='Enable monitor mode')
    monitor_parser.add_argument('interface', help='Network interface')
    
    managed_parser = subparsers.add_parser('managed', help='Disable monitor mode')
    managed_parser.add_argument('interface', help='Network interface')
    
    # Help commands
    subparsers.add_parser('help', help='Show help information')
    subparsers.add_parser('features', help='Show features matrix')
    subparsers.add_parser('commands', help='Show command reference')
    subparsers.add_parser('banner', help='Show banner')
    
    return parser


def main(argv: Optional[list] = None) -> int:
    """Main entry point."""
    parser = create_parser()
    args = parser.parse_args(argv or sys.argv[1:])
    
    # Show banner on startup
    if not args.command or args.command in ['help', 'banner']:
        print_banner()
        print_logo_large()
    
    if not args.command or args.command == 'help':
        parser.print_help()
        return 0
    
    elif args.command == 'features':
        print_features_matrix()
        return 0
    
    elif args.command == 'commands':
        print_quick_commands()
        return 0
    
    elif args.command == 'banner':
        print_logo_large()
        return 0
    
    elif args.command == 'scan':
        return handle_scan(args)
    
    elif args.command == 'auto':
        return handle_auto(args)
    
    elif args.command == 'crack':
        return handle_crack(args)
    
    elif args.command == 'monitor':
        return handle_monitor(args)
    
    elif args.command == 'managed':
        return handle_managed(args)
    
    else:
        parser.print_help()
        return 1


def handle_scan(args) -> int:
    """Handle scan command."""
    try:
        framework = WiFiPentestFramework(args.interface)
        
        if not framework.initialize():
            return 1
        
        networks = framework.scan_networks(args.duration)
        
        # Analyze security
        analyzer = EncryptionAnalyzer(framework.logger)
        analysis = analyzer.analyze_network_security(networks)
        
        # Print results
        print(f"\n{len(networks)} networks found:")
        for net in networks:
            print(f"  {net.ssid} ({net.bssid}) - {net.encryption}")
        
        framework.session_data['scan_results'] = {
            'networks': len(networks),
            'timestamp': str(analysis.get('scan_time'))
        }
        
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


def handle_auto(args) -> int:
    """Handle automated attack command."""
    try:
        framework = WiFiPentestFramework(args.interface)
        
        if not framework.initialize():
            return 1
        
        # Convert mode string to enum
        mode_map = {
            'passive': AttackMode.PASSIVE,
            'aggressive': AttackMode.AGGRESSIVE,
            'relentless': AttackMode.RELENTLESS,
            'stealth': AttackMode.STEALTH
        }
        mode = mode_map.get(args.mode, AttackMode.AGGRESSIVE)
        
        # Convert strategy string to enum
        strategy_map = {
            'wpa': AttackStrategy.WPA_ONLY,
            'wps': AttackStrategy.WPS_ONLY,
            'hybrid': AttackStrategy.HYBRID,
            'all': AttackStrategy.ALL
        }
        strategy = strategy_map.get(args.strategy, AttackStrategy.HYBRID)
        
        # Scan networks
        framework.logger.info("Scanning networks...")
        networks = framework.scan_networks(30)
        
        # Setup attacker
        attacker = AutomatedAttacker(framework)
        ranked = attacker.rank_targets(networks)
        
        if args.target:
            # Attack specific target
            target = next((net for net, _ in ranked if net.bssid == args.target), None)
            if target:
                result = attacker.attack(target, mode, strategy, args.wordlist or "rockyou.txt")
                print(f"Attack result: {result.success}")
        else:
            # Attack top targets
            targets = [net for net, _ in ranked[:3]]
            results = attacker.multi_target_attack(targets, mode, strategy, 
                                                  args.wordlist or "rockyou.txt")
            print(f"Completed {len(results)} attacks")
        
        return 0
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


def handle_crack(args) -> int:
    """Handle crack command."""
    try:
        framework = WiFiPentestFramework("wlan0")  # Dummy interface for cracking
        password = framework.crack_password(args.handshake, args.wordlist)
        
        if password:
            print(f"Password found: {password}")
            return 0
        else:
            print("Password not found")
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


def handle_monitor(args) -> int:
    """Handle monitor mode enable."""
    try:
        framework = WiFiPentestFramework(args.interface)
        framework.initialize()
        
        if framework.interface_detector.enable_monitor_mode(args.interface):
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


def handle_managed(args) -> int:
    """Handle monitor mode disable."""
    try:
        framework = WiFiPentestFramework(args.interface)
        framework.initialize()
        
        if framework.interface_detector.disable_monitor_mode(args.interface):
            return 0
        else:
            return 1
    except Exception as e:
        print(f"Error: {str(e)}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
