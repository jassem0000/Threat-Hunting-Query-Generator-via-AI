#!/usr/bin/env python3
"""
Test Runner Script for Threat Hunting Query Generator
This script runs all tests for the project.
"""

import subprocess
import sys
import os

def run_tests():
    """Run all tests for the project"""
    print("Running Threat Hunting Query Generator Tests")
    print("=" * 50)
    
    # Change to the project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    # Run the existing test file
    print("\n1. Running basic query generation test...")
    try:
        result = subprocess.run([
            sys.executable, 
            os.path.join(project_root, "tests", "test_query_generation.py")
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
    except Exception as e:
        print(f"Error running basic test: {e}")
    
    # Run the comprehensive test suite
    print("\n2. Running comprehensive test suite...")
    try:
        result = subprocess.run([
            sys.executable, 
            "-m", 
            "unittest", 
            "tests.test_threat_hunter",
            "-v"
        ], capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
            
        print(f"Return code: {result.returncode}")
    except Exception as e:
        print(f"Error running comprehensive test suite: {e}")
    
    print("\n" + "=" * 50)
    print("Test execution completed.")

if __name__ == "__main__":
    run_tests()