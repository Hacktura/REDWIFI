"""
Red WiFi Branding Module
Provides ASCII art, logos, and professional branding elements.
"""

# Color Constants
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BOLD = '\033[1m'
RESET = '\033[0m'


def print_banner():
    """Print professional welcome banner."""
    banner = f"""
{RED}╔═══════════════════════════════════════════════════════════════╗{RESET}
{RED}║                                                               ║{RESET}
{RED}║{CYAN}          🔴  RED WIFI v2.0 - WiFi Pentest Framework  🔴{RED}          ║{RESET}
{RED}║                                                               ║{RESET}
{RED}║{GREEN}              Professional Penetration Testing Tool{RED}              ║{RESET}
{RED}║{YELLOW}                   Built for Security Professionals{RED}             ║{RESET}
{RED}║                                                               ║{RESET}
{RED}╚═══════════════════════════════════════════════════════════════╝{RESET}
    """
    print(banner)


def print_logo_large():
    """Print large ASCII logo."""
    logo = f"""
{RED}
    ██████╗ ███████╗██████╗ ██╗    ██╗██╗███████╗██╗
    ██╔══██╗██╔════╝██╔══██╗██║    ██║██║██╔════╝██║
    ██████╔╝█████╗  ██║  ██║██║ █╗ ██║██║█████╗  ██║
    ██╔══██╗██╔══╝  ██║  ██║██║███╗██║██║██╔══╝  ██║
    ██║  ██║███████╗██████╔╝╚███╔███╔╝██║██║     ██║
    ╚═╝  ╚═╝╚══════╝╚═════╝  ╚══╝╚══╝ ╚═╝╚═╝     ╚═╝
{RESET}
    {CYAN}WiFi Penetration Testing Framework v2.0{RESET}
    """
    print(logo)


def print_quick_commands():
    """Print quick command reference."""
    reference = f"""
{BOLD}{CYAN}QUICK COMMAND REFERENCE{RESET}
{RED}═══════════════════════════════════════════════════════════════{RESET}

{GREEN}Basic Scanning:{RESET}
  red-wifi scan                    # Scan available networks
  red-wifi scan --monitor eth0     # Scan on specific interface

{GREEN}Automated Attacks:{RESET}
  red-wifi auto                    # Interactive attack menu
  red-wifi auto --target [BSSID]   # Target specific network
  red-wifi auto --aggressive       # Aggressive attack mode

{GREEN}Advanced Options:{RESET}
  red-wifi crack [HANDSHAKE.cap]   # Crack captured handshake
  red-wifi wps [BSSID]             # WPS vulnerability test
  red-wifi report [SESSION]        # Generate report

{GREEN}Utilities:{RESET}
  red-wifi monitor [INTERFACE]     # Enable monitor mode
  red-wifi managed [INTERFACE]     # Disable monitor mode
  red-wifi version                 # Show version info

{RED}═══════════════════════════════════════════════════════════════{RESET}
    """
    print(reference)


def print_features_matrix():
    """Print feature matrix."""
    features = f"""
{BOLD}{CYAN}FEATURES MATRIX{RESET}
{RED}═══════════════════════════════════════════════════════════════{RESET}

{GREEN}Attack Modes:{RESET}
  ✓ Passive Mode        (10-30 min, undetectable)
  ✓ Aggressive Mode     (2-5 min, standard detection)
  ✓ Relentless Mode     (1-2 min, high detection)
  ✓ Stealth Mode        (20-30 min, zero detection)

{GREEN}Cracking Methods:{RESET}
  ✓ Dictionary Attacks
  ✓ Rule-Based Attacks
  ✓ Hybrid Attacks
  ✓ Brute Force
  ✓ GPU Acceleration (hashcat)
  ✓ CPU Cracking (John)

{GREEN}Security Testing:{RESET}
  ✓ WPA/WPA2 Handshake Capture
  ✓ WPA3 Support
  ✓ WPS Pixie Dust Attacks
  ✓ WPS PIN Bruteforce
  ✓ Evil Twin Detection
  ✓ Client-Side Attacks
  ✓ Deauth Flooding

{GREEN}Professional Features:{RESET}
  ✓ Multi-Band Scanning (2.4GHz & 5GHz)
  ✓ Automated Target Selection
  ✓ Session Management
  ✓ JSON/HTML Reporting
  ✓ Color Console Output
  ✓ Progress Tracking
  ✓ Statistics Analysis
  ✓ Error Recovery

{RED}═══════════════════════════════════════════════════════════════{RESET}
    """
    print(features)


def print_attack_modes():
    """Print detailed attack mode descriptions."""
    modes = f"""
{BOLD}{CYAN}ATTACK MODES EXPLAINED{RESET}
{RED}═══════════════════════════════════════════════════════════════{RESET}

{GREEN}1. PASSIVE MODE{RESET}
   Duration: 10-30 minutes
   Detection: ★☆☆☆☆ (Undetectable)
   Method: Listen-only approach
   - Captures traffic without transmission
   - Waits for natural handshakes
   - Ideal for undetected research
   
{GREEN}2. AGGRESSIVE MODE{RESET}
   Duration: 2-5 minutes
   Detection: ★★★☆☆ (Standard)
   Method: Active deauth attacks
   - Sends deauth packets to force handshakes
   - Uses high power transmission
   - Standard penetration testing approach
   
{GREEN}3. RELENTLESS MODE{RESET}
   Duration: 1-2 minutes
   Detection: ★★★★★ (Highly detectable)
   Method: Intense attack flooding
   - Continuous deauth packets
   - Maximum aggression
   - Fastest results, highest risk
   
{GREEN}4. STEALTH MODE{RESET}
   Duration: 20-30 minutes
   Detection: ★☆☆☆☆ (Zero detection)
   Method: Low-power covert approach
   - Minimal power transmission
   - Longer wait times
   - Maximizes stealth and deniability

{RED}═══════════════════════════════════════════════════════════════{RESET}
    """
    print(modes)


def print_success_message(title):
    """Print success message with title."""
    message = f"""
{GREEN}╔════════════════════════════════════════════════════════════════╗{RESET}
{GREEN}║                                                                ║{RESET}
{GREEN}║{CYAN}                      ✓ SUCCESS{RED}                                   ║{RESET}
{GREEN}║{YELLOW}  {title.center(58)}{GREEN}  ║{RESET}
{GREEN}║                                                                ║{RESET}
{GREEN}╚════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(message)


def print_error_message(title):
    """Print error message with title."""
    message = f"""
{RED}╔════════════════════════════════════════════════════════════════╗{RESET}
{RED}║                                                                ║{RESET}
{RED}║                      ✗ ERROR{RESET}                                   {RED}║{RESET}
{RED}║{YELLOW}  {title.center(58)}{RED}  ║{RESET}
{RED}║                                                                ║{RESET}
{RED}╚════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(message)


def print_warning_message(title):
    """Print warning message with title."""
    message = f"""
{YELLOW}╔════════════════════════════════════════════════════════════════╗{RESET}
{YELLOW}║                                                                ║{RESET}
{YELLOW}║                      ⚠ WARNING{RESET}                                  {YELLOW}║{RESET}
{YELLOW}║{CYAN}  {title.center(58)}{YELLOW}  ║{RESET}
{YELLOW}║                                                                ║{RESET}
{YELLOW}╚════════════════════════════════════════════════════════════════╝{RESET}
    """
    print(message)


def format_table_header(*columns):
    """Format table header row."""
    col_width = 20
    header = f"{BOLD}{CYAN}"
    for col in columns:
        header += f"{col:<{col_width}}"
    header += f"{RESET}\n"
    header += f"{CYAN}{'─' * (col_width * len(columns))}{RESET}\n"
    return header


def format_table_row(*columns):
    """Format table data row."""
    col_width = 20
    row = ""
    for col in columns:
        row += f"{str(col):<{col_width}}"
    return row
