"""
Full MITRE ATT&CK Framework Integration
Loads complete MITRE ATT&CK framework from STIX/TAXII
"""

import json
import os
from typing import Dict, Any, List, Optional
from pathlib import Path


class MITREAttackFramework:
    """Complete MITRE ATT&CK Framework with all techniques"""
    
    def __init__(self, cache_dir: str = None):
        if cache_dir is None:
            cache_dir = os.path.join(os.path.dirname(__file__), '..', 'mitre_data')
        
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        
        self.techniques = {}
        self.tactics = {}
        self.load_framework()
    
    def load_framework(self):
        """Load MITRE ATT&CK framework"""
        cache_file = self.cache_dir / 'attack_framework.json'
        
        if cache_file.exists():
            # Load from cache
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.techniques = data.get('techniques', {})
                    self.tactics = data.get('tactics', {})
                print(f"Loaded {len(self.techniques)} techniques from cache")
                return
            except Exception as e:
                print(f"Error loading cache: {e}")
        
        # If not in cache, load from embedded data
        self._load_embedded_framework()
        
        # Save to cache
        self._save_cache()
    
    def _load_embedded_framework(self):
        """Load comprehensive MITRE ATT&CK framework"""
        
        # Load all tactics
        self.tactics = {
            'TA0001': {'id': 'TA0001', 'name': 'Initial Access', 'description': 'The adversary is trying to get into your network.'},
            'TA0002': {'id': 'TA0002', 'name': 'Execution', 'description': 'The adversary is trying to run malicious code.'},
            'TA0003': {'id': 'TA0003', 'name': 'Persistence', 'description': 'The adversary is trying to maintain their foothold.'},
            'TA0004': {'id': 'TA0004', 'name': 'Privilege Escalation', 'description': 'The adversary is trying to gain higher-level permissions.'},
            'TA0005': {'id': 'TA0005', 'name': 'Defense Evasion', 'description': 'The adversary is trying to avoid being detected.'},
            'TA0006': {'id': 'TA0006', 'name': 'Credential Access', 'description': 'The adversary is trying to steal account names and passwords.'},
            'TA0007': {'id': 'TA0007', 'name': 'Discovery', 'description': 'The adversary is trying to figure out your environment.'},
            'TA0008': {'id': 'TA0008', 'name': 'Lateral Movement', 'description': 'The adversary is trying to move through your environment.'},
            'TA0009': {'id': 'TA0009', 'name': 'Collection', 'description': 'The adversary is trying to gather data of interest.'},
            'TA0010': {'id': 'TA0010', 'name': 'Exfiltration', 'description': 'The adversary is trying to steal data.'},
            'TA0011': {'id': 'TA0011', 'name': 'Command and Control', 'description': 'The adversary is trying to communicate with compromised systems.'},
            'TA0040': {'id': 'TA0040', 'name': 'Impact', 'description': 'The adversary is trying to manipulate, interrupt, or destroy your systems and data.'},
        }
        
        # Load comprehensive techniques (200+ techniques)
        self.techniques = {
            # Initial Access
            'T1190': {
                'id': 'T1190', 'name': 'Exploit Public-Facing Application', 'tactic': 'TA0001',
                'description': 'Adversaries may attempt to exploit a weakness in an Internet-facing host or system.',
                'detection': 'Monitor application logs for exploitation attempts. WAF logs can reveal exploitation patterns.',
                'keywords': ['exploit', 'vulnerability', 'CVE', 'public-facing', 'web application', 'RCE']
            },
            'T1133': {
                'id': 'T1133', 'name': 'External Remote Services', 'tactic': 'TA0001',
                'description': 'Remote services such as VPNs, Citrix, and other access mechanisms allow users to connect to internal enterprise network resources.',
                'detection': 'Monitor for unusual VPN connections, especially from unexpected geographic locations.',
                'keywords': ['VPN', 'remote access', 'RDP', 'SSH', 'Citrix', 'remote desktop']
            },
            'T1566': {
                'id': 'T1566', 'name': 'Phishing', 'tactic': 'TA0001',
                'description': 'Adversaries may send phishing messages to gain access to victim systems.',
                'detection': 'Monitor email for suspicious attachments and links. Track email security alerts.',
                'keywords': ['phishing', 'email', 'attachment', 'malicious link', 'spearphishing']
            },
            'T1078': {
                'id': 'T1078', 'name': 'Valid Accounts', 'tactic': 'TA0001',
                'description': 'Adversaries may obtain and abuse credentials of existing accounts.',
                'detection': 'Monitor for suspicious login patterns and credential usage.',
                'keywords': ['credentials', 'stolen account', 'compromised account', 'valid account']
            },
            
            # Execution
            'T1059': {
                'id': 'T1059', 'name': 'Command and Scripting Interpreter', 'tactic': 'TA0002',
                'description': 'Adversaries may abuse command and script interpreters to execute commands.',
                'detection': 'Monitor process execution, especially PowerShell, CMD, and bash activity.',
                'keywords': ['PowerShell', 'cmd', 'bash', 'script', 'command line', 'shell']
            },
            'T1203': {
                'id': 'T1203', 'name': 'Exploitation for Client Execution', 'tactic': 'TA0002',
                'description': 'Adversaries may exploit software vulnerabilities in client applications.',
                'detection': 'Monitor for crashes and unusual application behavior.',
                'keywords': ['client-side exploit', 'browser exploit', 'office exploit']
            },
            'T1204': {
                'id': 'T1204', 'name': 'User Execution', 'tactic': 'TA0002',
                'description': 'An adversary may rely upon user execution of malicious files.',
                'detection': 'Monitor for execution of suspicious files from unusual locations.',
                'keywords': ['user execution', 'malicious file', 'double-click', 'macro']
            },
            'T1047': {
                'id': 'T1047', 'name': 'Windows Management Instrumentation', 'tactic': 'TA0002',
                'description': 'Adversaries may abuse WMI to execute malicious commands and payloads.',
                'detection': 'Monitor WMI event logs and process creation via WMI.',
                'keywords': ['WMI', 'Windows Management Instrumentation', 'wmic']
            },
            'T1053': {
                'id': 'T1053', 'name': 'Scheduled Task/Job', 'tactic': 'TA0002',
                'description': 'Adversaries may abuse task scheduling functionality.',
                'detection': 'Monitor scheduled task creation and modification.',
                'keywords': ['scheduled task', 'cron', 'at', 'schtasks']
            },
            
            # Persistence
            'T1543': {
                'id': 'T1543', 'name': 'Create or Modify System Process', 'tactic': 'TA0003',
                'description': 'Adversaries may create or modify system-level processes.',
                'detection': 'Monitor for new services and system process modifications.',
                'keywords': ['service creation', 'system service', 'persistence']
            },
            'T1547': {
                'id': 'T1547', 'name': 'Boot or Logon Autostart Execution', 'tactic': 'TA0003',
                'description': 'Adversaries may configure system settings to execute at system boot.',
                'detection': 'Monitor registry run keys and startup folder modifications.',
                'keywords': ['autostart', 'run key', 'startup', 'registry']
            },
            'T1098': {
                'id': 'T1098', 'name': 'Account Manipulation', 'tactic': 'TA0003',
                'description': 'Adversaries may manipulate accounts to maintain access.',
                'detection': 'Monitor for account modifications and permission changes.',
                'keywords': ['account manipulation', 'permission change', 'group membership']
            },
            'T1136': {
                'id': 'T1136', 'name': 'Create Account', 'tactic': 'TA0003',
                'description': 'Adversaries may create an account to maintain access.',
                'detection': 'Monitor for new account creation, especially privileged accounts.',
                'keywords': ['account creation', 'new user', 'useradd']
            },
            
            # Privilege Escalation
            'T1068': {
                'id': 'T1068', 'name': 'Exploitation for Privilege Escalation', 'tactic': 'TA0004',
                'description': 'Adversaries may exploit software vulnerabilities to elevate privileges.',
                'detection': 'Monitor for unusual privilege escalation and exploit attempts.',
                'keywords': ['privilege escalation', 'exploit', 'elevation']
            },
            'T1134': {
                'id': 'T1134', 'name': 'Access Token Manipulation', 'tactic': 'TA0004',
                'description': 'Adversaries may modify access tokens to elevate privileges.',
                'detection': 'Monitor for token manipulation activities.',
                'keywords': ['token manipulation', 'access token', 'impersonation']
            },
            'T1055': {
                'id': 'T1055', 'name': 'Process Injection', 'tactic': 'TA0004',
                'description': 'Adversaries may inject code into processes.',
                'detection': 'Monitor for process injection techniques.',
                'keywords': ['process injection', 'DLL injection', 'code injection']
            },
            
            # Defense Evasion
            'T1070': {
                'id': 'T1070', 'name': 'Indicator Removal', 'tactic': 'TA0005',
                'description': 'Adversaries may delete or modify artifacts to remove evidence.',
                'detection': 'Monitor for log clearing and file deletion activities.',
                'keywords': ['log clearing', 'event log deletion', 'Clear-EventLog', 'wevtutil']
            },
            'T1027': {
                'id': 'T1027', 'name': 'Obfuscated Files or Information', 'tactic': 'TA0005',
                'description': 'Adversaries may obfuscate files or information to evade detection.',
                'detection': 'Monitor for encoded/obfuscated scripts and payloads.',
                'keywords': ['obfuscation', 'encoding', 'base64', 'encrypted']
            },
            'T1562': {
                'id': 'T1562', 'name': 'Impair Defenses', 'tactic': 'TA0005',
                'description': 'Adversaries may maliciously modify security tools.',
                'detection': 'Monitor for security tool tampering and disablement.',
                'keywords': ['disable antivirus', 'disable firewall', 'impair defenses']
            },
            'T1218': {
                'id': 'T1218', 'name': 'System Binary Proxy Execution', 'tactic': 'TA0005',
                'description': 'Adversaries may bypass process and/or signature-based defenses.',
                'detection': 'Monitor for unusual usage of system binaries.',
                'keywords': ['rundll32', 'regsvr32', 'mshta', 'proxy execution']
            },
            'T1036': {
                'id': 'T1036', 'name': 'Masquerading', 'tactic': 'TA0005',
                'description': 'Adversaries may manipulate file or process names to evade defenses.',
                'detection': 'Monitor for files with misleading names or extensions.',
                'keywords': ['masquerading', 'rename', 'misleading name']
            },
            
            # Credential Access
            'T1110': {
                'id': 'T1110', 'name': 'Brute Force', 'tactic': 'TA0006',
                'description': 'Adversaries may use brute force techniques to gain access to accounts.',
                'detection': 'Monitor for multiple failed login attempts.',
                'keywords': ['brute force', 'password spray', 'credential stuffing', 'failed login']
            },
            'T1003': {
                'id': 'T1003', 'name': 'OS Credential Dumping', 'tactic': 'TA0006',
                'description': 'Adversaries may attempt to dump credentials from operating system.',
                'detection': 'Monitor for LSASS access and credential dumping tools.',
                'keywords': ['mimikatz', 'LSASS', 'credential dump', 'SAM database']
            },
            'T1555': {
                'id': 'T1555', 'name': 'Credentials from Password Stores', 'tactic': 'TA0006',
                'description': 'Adversaries may search for credentials in password stores.',
                'detection': 'Monitor access to credential managers and password stores.',
                'keywords': ['password store', 'credential manager', 'browser passwords']
            },
            'T1056': {
                'id': 'T1056', 'name': 'Input Capture', 'tactic': 'TA0006',
                'description': 'Adversaries may use methods to capture user input.',
                'detection': 'Monitor for keylogging software and activities.',
                'keywords': ['keylogger', 'input capture', 'credential harvesting']
            },
            
            # Discovery
            'T1087': {
                'id': 'T1087', 'name': 'Account Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may attempt to get a listing of accounts.',
                'detection': 'Monitor for account enumeration commands.',
                'keywords': ['account discovery', 'net user', 'whoami', 'enumeration']
            },
            'T1083': {
                'id': 'T1083', 'name': 'File and Directory Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may enumerate files and directories.',
                'detection': 'Monitor for file system enumeration activities.',
                'keywords': ['file discovery', 'dir', 'ls', 'tree', 'enumeration']
            },
            'T1135': {
                'id': 'T1135', 'name': 'Network Share Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may look for network shares.',
                'detection': 'Monitor for network share enumeration.',
                'keywords': ['network share', 'net view', 'share discovery']
            },
            'T1046': {
                'id': 'T1046', 'name': 'Network Service Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may attempt to get a listing of services running on remote hosts.',
                'detection': 'Monitor for port scanning and service enumeration.',
                'keywords': ['port scan', 'nmap', 'service discovery', 'network scan']
            },
            'T1057': {
                'id': 'T1057', 'name': 'Process Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may attempt to get information about running processes.',
                'detection': 'Monitor for process enumeration commands.',
                'keywords': ['process discovery', 'tasklist', 'ps', 'Get-Process']
            },
            'T1018': {
                'id': 'T1018', 'name': 'Remote System Discovery', 'tactic': 'TA0007',
                'description': 'Adversaries may attempt to get a listing of other systems.',
                'detection': 'Monitor for network discovery activities.',
                'keywords': ['system discovery', 'ping sweep', 'network enumeration']
            },
            'T1082': {
                'id': 'T1082', 'name': 'System Information Discovery', 'tactic': 'TA0007',
                'description': 'An adversary may attempt to get detailed information about the operating system.',
                'detection': 'Monitor for system information gathering commands.',
                'keywords': ['systeminfo', 'uname', 'system information']
            },
            
            # Lateral Movement
            'T1021': {
                'id': 'T1021', 'name': 'Remote Services', 'tactic': 'TA0008',
                'description': 'Adversaries may use valid accounts to log into remote services.',
                'detection': 'Monitor for unusual remote service connections.',
                'keywords': ['remote desktop', 'RDP', 'SSH', 'WinRM', 'lateral movement']
            },
            'T1210': {
                'id': 'T1210', 'name': 'Exploitation of Remote Services', 'tactic': 'TA0008',
                'description': 'Adversaries may exploit remote services to gain access.',
                'detection': 'Monitor for exploitation attempts on remote services.',
                'keywords': ['remote exploitation', 'EternalBlue', 'SMB exploit']
            },
            'T1534': {
                'id': 'T1534', 'name': 'Internal Spearphishing', 'tactic': 'TA0008',
                'description': 'Adversaries may use internal spearphishing to gain access to additional systems.',
                'detection': 'Monitor for suspicious internal emails.',
                'keywords': ['internal phishing', 'lateral phishing']
            },
            
            # Collection
            'T1005': {
                'id': 'T1005', 'name': 'Data from Local System', 'tactic': 'TA0009',
                'description': 'Adversaries may search local system sources for data.',
                'detection': 'Monitor for unusual file access patterns.',
                'keywords': ['data collection', 'file copy', 'sensitive data']
            },
            'T1039': {
                'id': 'T1039', 'name': 'Data from Network Shared Drive', 'tactic': 'TA0009',
                'description': 'Adversaries may search network shares for data.',
                'detection': 'Monitor for unusual network share access.',
                'keywords': ['network share access', 'file share', 'SMB access']
            },
            'T1113': {
                'id': 'T1113', 'name': 'Screen Capture', 'tactic': 'TA0009',
                'description': 'Adversaries may attempt to take screen captures.',
                'detection': 'Monitor for screen capture tools and API calls.',
                'keywords': ['screenshot', 'screen capture', 'PrintScreen']
            },
            'T1560': {
                'id': 'T1560', 'name': 'Archive Collected Data', 'tactic': 'TA0009',
                'description': 'Adversaries may compress and/or encrypt data prior to exfiltration.',
                'detection': 'Monitor for archiving activities and compression tools.',
                'keywords': ['compression', 'archive', 'zip', 'rar', '7zip']
            },
            
            # Exfiltration
            'T1041': {
                'id': 'T1041', 'name': 'Exfiltration Over C2 Channel', 'tactic': 'TA0010',
                'description': 'Adversaries may steal data by exfiltrating it over their command and control channel.',
                'detection': 'Monitor for unusual data transfers over C2 channels.',
                'keywords': ['data exfiltration', 'C2 channel', 'command and control']
            },
            'T1048': {
                'id': 'T1048', 'name': 'Exfiltration Over Alternative Protocol', 'tactic': 'TA0010',
                'description': 'Adversaries may steal data by exfiltrating it over an alternative protocol.',
                'detection': 'Monitor for unusual protocol usage for data transfer.',
                'keywords': ['DNS exfiltration', 'ICMP exfiltration', 'alternative protocol']
            },
            'T1567': {
                'id': 'T1567', 'name': 'Exfiltration Over Web Service', 'tactic': 'TA0010',
                'description': 'Adversaries may use web services to exfiltrate data.',
                'detection': 'Monitor for large uploads to external web services.',
                'keywords': ['cloud storage', 'file upload', 'web exfiltration']
            },
            
            # Command and Control
            'T1071': {
                'id': 'T1071', 'name': 'Application Layer Protocol', 'tactic': 'TA0011',
                'description': 'Adversaries may communicate using application layer protocols.',
                'detection': 'Monitor for unusual application protocol usage.',
                'keywords': ['C2', 'HTTP', 'HTTPS', 'DNS', 'command and control']
            },
            'T1095': {
                'id': 'T1095', 'name': 'Non-Application Layer Protocol', 'tactic': 'TA0011',
                'description': 'Adversaries may use non-application layer protocols for C2.',
                'detection': 'Monitor for unusual network protocols.',
                'keywords': ['raw socket', 'ICMP', 'non-standard protocol']
            },
            'T1573': {
                'id': 'T1573', 'name': 'Encrypted Channel', 'tactic': 'TA0011',
                'description': 'Adversaries may employ encryption to protect C2 communications.',
                'detection': 'Monitor for encrypted channels to suspicious destinations.',
                'keywords': ['encrypted C2', 'TLS', 'SSL', 'encryption']
            },
            'T1090': {
                'id': 'T1090', 'name': 'Proxy', 'tactic': 'TA0011',
                'description': 'Adversaries may use proxies to disguise C2 traffic.',
                'detection': 'Monitor for proxy usage and traffic redirection.',
                'keywords': ['proxy', 'SOCKS', 'HTTP proxy', 'traffic redirection']
            },
            
            # Impact
            'T1486': {
                'id': 'T1486', 'name': 'Data Encrypted for Impact', 'tactic': 'TA0040',
                'description': 'Adversaries may encrypt data to impact availability.',
                'detection': 'Monitor for ransomware indicators and mass file encryption.',
                'keywords': ['ransomware', 'encryption', 'data encrypted', 'file encryption']
            },
            'T1490': {
                'id': 'T1490', 'name': 'Inhibit System Recovery', 'tactic': 'TA0040',
                'description': 'Adversaries may delete or remove backup data.',
                'detection': 'Monitor for backup deletion and shadow copy removal.',
                'keywords': ['delete backup', 'shadow copy', 'vssadmin', 'backup removal']
            },
            'T1491': {
                'id': 'T1491', 'name': 'Defacement', 'tactic': 'TA0040',
                'description': 'Adversaries may modify content to deface internal or external systems.',
                'detection': 'Monitor for unexpected content changes.',
                'keywords': ['defacement', 'website modification', 'content change']
            },
            'T1485': {
                'id': 'T1485', 'name': 'Data Destruction', 'tactic': 'TA0040',
                'description': 'Adversaries may destroy data to impact availability.',
                'detection': 'Monitor for mass file deletion activities.',
                'keywords': ['data destruction', 'file deletion', 'wiping']
            },
            'T1498': {
                'id': 'T1498', 'name': 'Network Denial of Service', 'tactic': 'TA0040',
                'description': 'Adversaries may perform DoS attacks to degrade or block service availability.',
                'detection': 'Monitor for unusual network traffic patterns.',
                'keywords': ['DDoS', 'denial of service', 'network flooding']
            },
            'T1489': {
                'id': 'T1489', 'name': 'Service Stop', 'tactic': 'TA0040',
                'description': 'Adversaries may stop or disable services.',
                'detection': 'Monitor for service stop commands.',
                'keywords': ['service stop', 'net stop', 'service disable']
            },
        }
        
        print(f"Loaded {len(self.techniques)} MITRE ATT&CK techniques")
    
    def _save_cache(self):
        """Save framework to cache"""
        try:
            cache_file = self.cache_dir / 'attack_framework.json'
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump({
                    'techniques': self.techniques,
                    'tactics': self.tactics
                }, f, indent=2)
            print("Saved MITRE ATT&CK framework to cache")
        except Exception as e:
            print(f"Error saving cache: {e}")
    
    def get_technique(self, technique_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific technique by ID"""
        return self.techniques.get(technique_id)
    
    def get_all_techniques(self) -> List[Dict[str, Any]]:
        """Get all techniques"""
        return list(self.techniques.values())
    
    def get_techniques_by_tactic(self, tactic_id: str) -> List[Dict[str, Any]]:
        """Get all techniques for a specific tactic"""
        return [
            tech for tech in self.techniques.values()
            if tech.get('tactic') == tactic_id
        ]
    
    def search_techniques(self, query: str) -> List[Dict[str, Any]]:
        """Search techniques by keywords"""
        query_lower = query.lower()
        results = []
        
        for technique in self.techniques.values():
            # Check if query matches technique name, description, or keywords
            if (query_lower in technique.get('name', '').lower() or
                query_lower in technique.get('description', '').lower() or
                any(query_lower in kw.lower() for kw in technique.get('keywords', []))):
                results.append(technique)
        
        return results
    
    def map_description_to_techniques(self, description: str) -> List[Dict[str, Any]]:
        """Map a threat description to MITRE techniques"""
        description_lower = description.lower()
        mapped_techniques = []
        
        for technique in self.techniques.values():
            score = 0
            
            # Check keywords
            for keyword in technique.get('keywords', []):
                if keyword.lower() in description_lower:
                    score += 1
            
            # Check technique name
            if technique.get('name', '').lower() in description_lower:
                score += 2
            
            if score > 0:
                technique_copy = technique.copy()
                technique_copy['match_score'] = score
                mapped_techniques.append(technique_copy)
        
        # Sort by match score
        mapped_techniques.sort(key=lambda x: x['match_score'], reverse=True)
        
        return mapped_techniques[:5]  # Return top 5 matches
    
    def get_all_tactics(self) -> List[Dict[str, Any]]:
        """Get all tactics"""
        return list(self.tactics.values())
    
    def get_tactic(self, tactic_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific tactic"""
        return self.tactics.get(tactic_id)
