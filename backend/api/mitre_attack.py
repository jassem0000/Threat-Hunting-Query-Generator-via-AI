from typing import List, Dict, Any
import requests
import json

class MitreAttackIntegration:
    """Integrates with MITRE ATT&CK framework for technique mapping"""
    
    def __init__(self):
        """Initialize MITRE ATT&CK integration"""
        self.attack_url = "https://raw.githubusercontent.com/mitre/cti/master/enterprise-attack/enterprise-attack.json"
        self.techniques = {}
        self._load_techniques()
    
    def _load_techniques(self):
        """Load MITRE ATT&CK techniques from GitHub"""
        try:
            # In a production environment, you would load this from the TAXII server
            # For this prototype, we'll use a simplified approach with sample data
            self.techniques = {
                "T1078": {
                    "name": "Valid Accounts",
                    "description": "Adversaries may obtain and abuse credentials of existing accounts as a means of gaining Initial Access, Persistence, Privilege Escalation, or Defense Evasion."
                },
                "T1110": {
                    "name": "Brute Force",
                    "description": "Adversaries may use brute force techniques to gain access to accounts when passwords are unknown or when password hashes are obtained."
                },
                "T1059": {
                    "name": "Command and Scripting Interpreter",
                    "description": "Adversaries may abuse command and script interpreters to execute commands, scripts, or binaries."
                },
                "T1041": {
                    "name": "Exfiltration Over C2 Channel",
                    "description": "Adversaries may steal data by exfiltrating it over an existing command and control channel."
                },
                "T1055": {
                    "name": "Process Injection",
                    "description": "Adversaries may inject code into processes in order to evade process-based defenses as well as possibly elevate privileges."
                }
            }
        except Exception as e:
            print(f"Warning: Could not load MITRE ATT&CK techniques: {e}")
            # Fallback to empty dict
            self.techniques = {}
    
    def map_to_technique(self, description: str) -> Dict[str, Any]:
        """
        Map a threat description to a MITRE ATT&CK technique
        
        Args:
            description: Natural language description of the threat
            
        Returns:
            Dictionary with technique information
        """
        # This is a simplified implementation
        # In a real system, you would use NLP or keyword matching to find the best technique
        description_lower = description.lower()
        
        # Simple keyword matching
        if "brute" in description_lower or "password" in description_lower:
            return self.techniques.get("T1110", {})
        elif "valid account" in description_lower or "credential" in description_lower:
            return self.techniques.get("T1078", {})
        elif "script" in description_lower or "command" in description_lower:
            return self.techniques.get("T1059", {})
        elif "exfiltration" in description_lower or "data leak" in description_lower:
            return self.techniques.get("T1041", {})
        elif "process injection" in description_lower or "dll" in description_lower:
            return self.techniques.get("T1055", {})
        else:
            # Return a generic technique if no match found
            return {
                "technique_id": "T0000",
                "name": "Unknown Technique",
                "description": "No matching MITRE ATT&CK technique found for the given description."
            }
    
    def get_all_techniques(self) -> List[Dict[str, Any]]:
        """
        Get all loaded MITRE ATT&CK techniques
        
        Returns:
            List of technique dictionaries
        """
        return [
            {"id": tech_id, **tech_data} 
            for tech_id, tech_data in self.techniques.items()
        ]