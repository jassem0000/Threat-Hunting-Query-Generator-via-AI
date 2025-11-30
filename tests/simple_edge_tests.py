#!/usr/bin/env python3
"""
Simple Edge Case Tests for Threat Hunting Query Generator
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.query_generator import QueryGenerator
from api.validators import QueryValidator
from api.mitre_attack import MitreAttackIntegration

def test_simple_edge_cases():
    """Test simple edge cases"""
    
    print("Simple Edge Case Tests")
    print("=" * 25)
    
    # Initialize components
    generator = QueryGenerator()
    validator = QueryValidator()
    mitre = MitreAttackIntegration()
    
    # Test 1: Empty description
    print("\n1. Empty Description Test")
    try:
        result = generator.generate("", "spl")
        print(f"   ✅ Handled empty description")
        print(f"   Query: {result['query'][:50]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Invalid query type
    print("\n2. Invalid Query Type Test")
    try:
        result = generator.generate("Test description", "invalid")
        print(f"   ❌ Should have raised an error")
    except ValueError as e:
        print(f"   ✅ Correctly raised ValueError: {e}")
    except Exception as e:
        print(f"   ⚠️  Unexpected error: {e}")
    
    # Test 3: None validation
    print("\n3. None Validation Test")
    try:
        result = validator.validate(None, "spl")
        print(f"   ✅ Handled None input")
        print(f"   Valid: {result['valid']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Empty string validation
    print("\n4. Empty String Validation Test")
    try:
        result = validator.validate("", "spl")
        print(f"   ✅ Handled empty string")
        print(f"   Valid: {result['valid']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Special characters in description
    print("\n5. Special Characters Test")
    special_desc = "Detect attacks with @#$%^&*() characters"
    try:
        result = generator.generate(special_desc, "spl")
        print(f"   ✅ Handled special characters")
        print(f"   Query: {result['query'][:50]}...")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 25)
    print("Simple edge case testing completed!")

if __name__ == "__main__":
    test_simple_edge_cases()