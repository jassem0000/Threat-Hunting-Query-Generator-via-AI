#!/usr/bin/env python3
"""
Practical Example Script for Threat Hunting Query Generator

This script demonstrates how to use the threat hunting query generator
with real-world threat hunting scenarios.
"""

import sys
import os
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.query_generator import QueryGenerator
from api.validators import QueryValidator
from api.mitre_attack import MitreAttackIntegration

def demonstrate_threat_hunting():
    """Demonstrate the threat hunting query generator with practical examples"""
    
    print("Threat Hunting Query Generator - Practical Examples")
    print("=" * 55)
    
    # Initialize components
    generator = QueryGenerator()
    validator = QueryValidator()
    mitre = MitreAttackIntegration()
    
    # Real-world threat hunting scenarios
    scenarios = [
        {
            "name": "Brute Force Attack Detection",
            "description": "Find all failed login attempts from external IP addresses in the last 24 hours that exceed 10 attempts per IP",
            "mitre_technique": "T1110 - Brute Force"
        },
        {
            "name": "Suspicious PowerShell Activity",
            "description": "Identify PowerShell processes that execute encoded commands or download content from suspicious domains",
            "mitre_technique": "T1059 - Command and Scripting Interpreter"
        },
        {
            "name": "Data Exfiltration Detection",
            "description": "Detect large outbound network transfers to external IPs that are not part of known business partners",
            "mitre_technique": "T1041 - Exfiltration Over C2 Channel"
        },
        {
            "name": "Lateral Movement Detection",
            "description": "Find authentication attempts from a single user account to multiple hosts within a short timeframe",
            "mitre_technique": "T1078 - Valid Accounts"
        },
        {
            "name": "Credential Dumping Detection",
            "description": "Detect processes that access LSASS memory or execute known credential dumping tools like mimikatz",
            "mitre_technique": "T1003 - OS Credential Dumping"
        }
    ]
    
    # Process each scenario
    for i, scenario in enumerate(scenarios, 1):
        print(f"\n{i}. {scenario['name']}")
        print("-" * len(f"{i}. {scenario['name']}"))
        print(f"Description: {scenario['description']}")
        print(f"MITRE ATT&CK: {scenario['mitre_technique']}")
        
        # Generate queries for each platform
        query_types = [
            ("Splunk SPL", "spl"),
            ("KQL (Sentinel)", "kql"),
            ("Elasticsearch DSL", "dsl")
        ]
        
        for platform_name, query_type in query_types:
            print(f"\n  {platform_name}:")
            try:
                # Generate query
                result = generator.generate(scenario['description'], query_type)
                
                # Display generated query
                print(f"    Query: {result['query']}")
                
                # Display explanation
                print(f"    Explanation: {result['explanation']}")
                
                # Validate query
                validation = validator.validate(result['query'], query_type)
                status = "✅ Valid" if validation['valid'] else "❌ Invalid"
                print(f"    Validation: {status}")
                
                # Show validation details if there are issues
                if not validation['valid']:
                    if validation['errors']:
                        print(f"      Errors: {', '.join(validation['errors'])}")
                    if validation['warnings']:
                        print(f"      Warnings: {', '.join(validation['warnings'])}")
                
                # Show optimization suggestions
                if validation['optimization_suggestions']:
                    print(f"    Suggestions: {', '.join(validation['optimization_suggestions'])}")
                    
            except Exception as e:
                print(f"    ❌ Error: {str(e)}")
        
        # MITRE ATT&CK mapping
        try:
            mitre_result = mitre.map_to_technique(scenario['description'])
            if mitre_result and mitre_result.get('name'):
                print(f"  MITRE Mapping: {mitre_result.get('name')} ({mitre_result.get('technique_id', 'N/A')})")
                print(f"    Description: {mitre_result.get('description', 'N/A')}")
        except Exception as e:
            print(f"  MITRE Mapping: Error - {str(e)}")
        
        print("\n" + "="*55)

def interactive_mode():
    """Interactive mode for testing custom threat descriptions"""
    print("\nInteractive Mode")
    print("=" * 15)
    print("Enter your own threat hunting descriptions to generate queries.")
    print("Type 'quit' to exit.\n")
    
    generator = QueryGenerator()
    validator = QueryValidator()
    mitre = MitreAttackIntegration()
    
    while True:
        description = input("Enter threat description: ").strip()
        
        if description.lower() in ['quit', 'exit', 'q']:
            break
            
        if not description:
            print("Please enter a valid description.\n")
            continue
            
        print("\nGenerating queries...\n")
        
        # Generate for all platforms
        for query_type, type_name in [("spl", "Splunk SPL"), ("kql", "KQL"), ("dsl", "Elasticsearch DSL")]:
            try:
                result = generator.generate(description, query_type)
                print(f"{type_name}:")
                print(f"  Query: {result['query']}")
                print(f"  Explanation: {result['explanation']}")
                
                validation = validator.validate(result['query'], query_type)
                status = "✅ Valid" if validation['valid'] else "❌ Invalid"
                print(f"  Validation: {status}\n")
            except Exception as e:
                print(f"{type_name}: Error - {str(e)}\n")
        
        # MITRE mapping
        try:
            mitre_result = mitre.map_to_technique(description)
            if mitre_result and mitre_result.get('name'):
                print(f"MITRE ATT&CK: {mitre_result.get('name')}")
        except Exception as e:
            print(f"MITRE Mapping: Error - {str(e)}")
        
        print("-" * 50)

if __name__ == "__main__":
    # Run demonstrations
    demonstrate_threat_hunting()
    
    # Offer interactive mode
    choice = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
    if choice in ['y', 'yes']:
        interactive_mode()
    
    print("\nDemo completed!")