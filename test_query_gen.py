#!/usr/bin/env python3
"""
Simple test script to verify query generation is working
"""

import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from api.query_generator import QueryGenerator

def test_query_generation():
    """Test query generation with a simple example"""
    print("Testing Query Generation...")
    print("=" * 30)
    
    # Initialize the query generator
    generator = QueryGenerator()
    
    # Test description
    description = "Find all failed login attempts in the last hour"
    
    print(f"Input description: {description}")
    print()
    
    # Test all query types
    query_types = ["spl", "kql", "dsl"]
    
    for query_type in query_types:
        print(f"Generating {query_type.upper()} query...")
        try:
            result = generator.generate(description, query_type)
            print(f"  Query: {result['query']}")
            print(f"  Explanation: {result['explanation']}")
            print()
        except Exception as e:
            print(f"  Error: {e}")
            print()
    
    print("Test completed!")

if __name__ == "__main__":
    test_query_generation()