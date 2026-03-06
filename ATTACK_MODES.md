# Attack Modes Guide

Detailed explanation of Red WiFi attack modes and strategies.

## Attack Modes Overview

Red WiFi provides four distinct attack modes, each optimized for different scenarios:

### 1. PASSIVE Mode

**Duration**: 10-30 minutes  
**Detection Risk**: ★☆☆☆☆ (Undetectable)  
**Aggression**: Minimal  
**Best For**: Stealth operations, hidden testing

#### How It Works
- Listens for natural client associations
- No active transmission
- Waits for clients to connect naturally
- Captures handshakes without alerting network

#### Advantages
- Zero detection risk
- Professional approach
- Leaves no obvious traces
- Ideal for covert assessment

#### Disadvantages
- Requires patience (long wait times)
- Dependent on client behavior
- May not capture if no clients connect
- Slower than other modes

#### When to Use
- Educational environment (teach stealth)
- Red team exercise with no discovery desired
- Network with tight security monitoring
- Long-term covert assessment

#### Command Example
```bash
red-wifi auto --interface wlan0 --mode passive
```

---

### 2. AGGRESSIVE Mode

**Duration**: 2-5 minutes  
**Detection Risk**: ★★★☆☆ (Standard)  
**Aggression**: Moderate  
**Best For**: Standard penetration testing

#### How It Works
- Sends deauthentication packets
- Forces clients to reconnect
- Captures full 4-way handshake
- Balanced speed and detection

#### Advantages
- Good speed (2-5 minutes typical)
- Reliable handshake capture
- Industry standard approach
- Suitable for most situations

#### Disadvantages
- Clients notice disconnection
- IDS may detect deauth packets
- Some network monitoring tools will alert
- Not suitable for stealth

#### When to Use
- Standard penetration test
- Authorized security assessment
- When speed is important
- Red team exercises
- Client knows testing is happening

#### Command Example
```bash
red-wifi auto --interface wlan0 --mode aggressive
```

---

### 3. RELENTLESS Mode

**Duration**: 1-2 minutes  
**Detection Risk**: ★★★★★ (Highly Detectable)  
**Aggression**: Maximum  
**Best For**: Quick proof-of-concept, authorized testing

#### How It Works
- Continuous deauth packet flooding
- Maximum transmission power
- Forceful client disconnection
- Very fast operation

#### Advantages
- Fastest handshake capture (1-2 min)
- Nearly guaranteed success
- Simple and direct
- Suitable for demo/proof-of-concept

#### Disadvantages
- Obvious to any observer
- Will trigger network alarms
- Disruptive to network service
- Not suitable for stealth testing
- May prevent legitimate connections

#### When to Use
- Proof-of-concept demo
- Authorized penetration test with client knowledge
- Lab environment testing
- Red team exercise (when discovery accepted)
- Quick vulnerability demonstration

#### Command Example
```bash
red-wifi auto --interface wlan0 --mode relentless
```

---

### 4. STEALTH Mode

**Duration**: 20-30 minutes  
**Detection Risk**: ★☆☆☆☆ (Zero Detection)  
**Aggression**: Very Low  
**Best For**: Professional covert operations

#### How It Works
- Low power transmission
- Subtle client nudging
- Long observation period
- Minimal network disruption

#### Advantages
- Virtually undetectable
- Minimal network impact
- Professional approach
- No obvious interference

#### Disadvantages
- Very slow (20-30 minutes)
- Requires patience
- Still technically active (not true passive)
- May not work if no clients around

#### When to Use
- Covert assessment where discovery is bad
- Competitive analysis
- Security validation (low disruption)
- Long-term monitoring capability
- Professional red team operations

#### Command Example
```bash
red-wifi auto --interface wlan0 --mode stealth
```

---

## Mode Comparison Table

| Aspect | Passive | Aggressive | Relentless | Stealth |
|--------|---------|-----------|-----------|---------|
| Duration | 10-30 min | 2-5 min | 1-2 min | 20-30 min |
| Detection | ★☆☆☆☆ | ★★★☆☆ | ★★★★★ | ★☆☆☆☆ |
| Success Rate | 70-80% | 95%+ | 99%+ | 85-90% |
| Network Impact | None | Moderate | High | Minimal |
| Packet Transmission | None | Moderate | Maximum | Minimal |
| Best Use Case | Stealth | Standard | Demo | Professional |
| Equipment Needed | Passive | Active | Active | Active |

---

## Attack Strategies

Red WiFi supports multiple attack strategies to target different vulnerabilities:

### WPA_ONLY Strategy

Focus exclusively on WPA/WPA2/WPA3 vulnerabilities:
- Dictionary attacks
- Rule-based attacks
- Hybrid attacks
- GPU-accelerated cracking

```bash
red-wifi auto --interface wlan0 --strategy wpa
```

### WPS_ONLY Strategy

Target WPS vulnerabilities:
- Pixie Dust attacks
- PIN bruteforce
- Reaver integration

```bash
red-wifi auto --interface wlan0 --strategy wps
```

### HYBRID Strategy

Combine WPA and WPS attacks:
- Try both methods simultaneously
- Fastest overall success rate
- Recommended for most situations

```bash
red-wifi auto --interface wlan0 --strategy hybrid
```

### ALL Strategy

Comprehensive attack using all methods:
- WPA cracking
- WPS exploitation
- Client-side attacks
- Advanced techniques

```bash
red-wifi auto --interface wlan0 --strategy all
```

---

## Attack Selection Matrix

Choose the right combination for your needs:

```
                     WPA Strong?
            Yes             No
         /-------\      /-------\
    WPS  |       |      |       |
    On? Y| HYB   |  N  | WPS   |
         |RELENT |      | RELENT|
         \-------/      \-------/

    N    | WPA   |      | SKIP  |
         | PASS  |      | (Open)|
         \-------/      \-------/
```

---

## Advanced: Custom Mode Configuration

Create custom attack modes by combining settings:

```python
from red_wifi import *

class CustomMode:
    """Custom attack mode combining multiple techniques."""
    
    def __init__(self, framework):
        self.framework = framework
        self.attacker = AutomatedAttacker(framework)
    
    def custom_attack(self, target):
        """Execute custom attack sequence."""
        
        # Phase 1: Passive listening (5 min)
        print("Phase 1: Passive Listening")
        # ... passive code ...
        
        # Phase 2: Active deauth (2 min)
        print("Phase 2: Active Deauth")
        # ... active code ...
        
        # Phase 3: Cracking (parallel)
        print("Phase 3: Parallel Cracking")
        # ... cracking code ...
```

---

## Mode Selection Decision Tree

```
Start: Choose attack mode

Does client want stealth?
├─ YES: Discovery = bad
│   └─ PASSIVE or STEALTH
│       ├─ Want fastest stealth?
│       │   └─ STEALTH (30 min, very hidden)
│       └─ Want guaranteed capture?
│           └─ PASSIVE (longer, safest)
│
└─ NO: Discovery = acceptable
    └─ AGGRESSIVE or RELENTLESS
        ├─ Want standard assessment?
        │   └─ AGGRESSIVE (2-5 min, balanced)
        └─ Want fastest demo?
            └─ RELENTLESS (1-2 min, obvious)
```

---

## Performance Benchmarks

Typical capture times by scenario:

### Scenario 1: Active Client (downloading)
- Passive: 2-5 minutes
- Aggressive: 30 seconds - 2 minutes
- Relentless: 10-30 seconds
- Stealth: 10-15 minutes

### Scenario 2: Idle Client (online but inactive)
- Passive: 10-20 minutes
- Aggressive: 1-3 minutes
- Relentless: 30-60 seconds
- Stealth: 15-25 minutes

### Scenario 3: No Active Clients
- Passive: 20-30 minutes
- Aggressive: 2-5 minutes (requires client)
- Relentless: 1-2 minutes (requires client)
- Stealth: 20-30 minutes

---

## Tips for Success

### Passive/Stealth Success
- Wait longer than expected
- Position near target network
- Monitor multiple channels
- Multiple capture attempts

### Aggressive/Relentless Success
- Ensure monitor mode enabled
- Good signal strength (-50 to -70 dBm)
- Network actually online
- Compatible with adapter

### Cracking Success
- Use optimized wordlist
- Try multiple methods (hashcat, john)
- Verify handshake validity
- Use GPU if available

---

## Legal and Ethical Considerations

**Important**: Always ensure:
1. Written authorization from network owner
2. Compliance with local laws
3. Appropriate mode for environment
4. Proper documentation

Different modes have different operational security implications.

---

For more information, see [USAGE.md](USAGE.md) and [FAQ.md](FAQ.md).
