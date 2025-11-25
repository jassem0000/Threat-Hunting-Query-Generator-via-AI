import sys
import os
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.query_generator import QueryGenerator
from api.validators import QueryValidator
from api.mitre_attack import MitreAttackIntegration

def test_query_generator():
    """Test the query generator with sample inputs"""
    print("Testing Query Generator...")
    
    # Initialize components
    generator = QueryGenerator()
    validator = QueryValidator()
    mitre = MitreAttackIntegration()
    
    # Test cases
    test_cases = [
        {
            "description": "Find all failed login attempts from external IP addresses in the last 24 hours",
            "query_types": ["spl", "kql", "dsl"]
        },
        {
            "description": "Identify suspicious PowerShell activity that may indicate malicious script execution",
            "query_types": ["spl", "kql", "dsl"]
        }
    ]
    
    for i, test_case in enumerate(test_cases):
        print(f"\nTest Case {i+1}: {test_case['description']}")
        
        for query_type in test_case['query_types']:
            print(f"  Testing {query_type.upper()} query generation...")
            
            try:
                # Generate query
                result = generator.generate(test_case['description'], query_type)
                print(f"    Generated query: {result['query'][:100]}...")
                print(f"    Explanation: {result['explanation'][:100]}...")
                
                # Validate query
                validation = validator.validate(result['query'], query_type)
                print(f"    Validation: {'Valid' if validation['valid'] else 'Invalid'}")
                
                # MITRE mapping
                mitre_result = mitre.map_to_technique(test_case['description'])
                print(f"    MITRE Technique: {mitre_result.get('name', 'None')}")
                
            except Exception as e:
                print(f"    Error: {str(e)}")
    
    print("\nTest completed.")

if __name__ == "__main__":
    test_query_generator()