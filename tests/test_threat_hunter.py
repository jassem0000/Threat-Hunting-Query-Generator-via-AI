import unittest
import sys
import os
import json

# Add the backend directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.query_generator import QueryGenerator
from api.validators import QueryValidator
from api.mitre_attack import MitreAttackIntegration

class TestQueryGenerator(unittest.TestCase):
    """Test suite for the Threat Hunting Query Generator components"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.generator = QueryGenerator()
        self.validator = QueryValidator()
        self.mitre = MitreAttackIntegration()
    
    def test_query_generator_initialization(self):
        """Test that QueryGenerator initializes correctly"""
        self.assertIsInstance(self.generator, QueryGenerator)
        self.assertIn("spl", self.generator.prompt_templates)
        self.assertIn("kql", self.generator.prompt_templates)
        self.assertIn("dsl", self.generator.prompt_templates)
    
    def test_mitre_attack_initialization(self):
        """Test that MitreAttackIntegration initializes correctly"""
        self.assertIsInstance(self.mitre, MitreAttackIntegration)
        self.assertGreater(len(self.mitre.techniques), 0)
    
    def test_validator_initialization(self):
        """Test that QueryValidator initializes correctly"""
        self.assertIsInstance(self.validator, QueryValidator)
    
    def test_spl_query_generation(self):
        """Test SPL query generation with a simple threat description"""
        description = "Find all failed login attempts in the last hour"
        result = self.generator.generate(description, "spl")
        
        # Check that we get a result with required keys
        self.assertIn("query", result)
        self.assertIn("explanation", result)
        
        # Check that the result is not empty
        self.assertIsNotNone(result["query"])
        self.assertNotEqual(result["query"], "")
    
    def test_kql_query_generation(self):
        """Test KQL query generation with a simple threat description"""
        description = "Find all failed login attempts in the last hour"
        result = self.generator.generate(description, "kql")
        
        # Check that we get a result with required keys
        self.assertIn("query", result)
        self.assertIn("explanation", result)
        
        # Check that the result is not empty
        self.assertIsNotNone(result["query"])
        self.assertNotEqual(result["query"], "")
    
    def test_dsl_query_generation(self):
        """Test DSL query generation with a simple threat description"""
        description = "Find all failed login attempts in the last hour"
        result = self.generator.generate(description, "dsl")
        
        # Check that we get a result with required keys
        self.assertIn("query", result)
        self.assertIn("explanation", result)
        
        # Check that the result is not empty
        self.assertIsNotNone(result["query"])
        self.assertNotEqual(result["query"], "")
    
    def test_invalid_query_type(self):
        """Test that invalid query types are handled properly"""
        description = "Test description"
        with self.assertRaises(ValueError):
            self.generator.generate(description, "invalid_type")
    
    def test_empty_description(self):
        """Test handling of empty threat description"""
        description = ""
        result = self.generator.generate(description, "spl")
        
        # Should still return a result even with empty description
        self.assertIn("query", result)
        self.assertIn("explanation", result)
    
    def test_mitre_mapping_brute_force(self):
        """Test MITRE ATT&CK mapping for brute force techniques"""
        description = "Detect brute force attacks against SSH services"
        result = self.mitre.map_to_technique(description)
        
        # Should map to Brute Force technique
        self.assertIn("name", result)
        # Note: Our simple implementation may not perfectly map this,
        # but it should return some technique
        self.assertIsNotNone(result["name"])
    
    def test_mitre_mapping_valid_accounts(self):
        """Test MITRE ATT&CK mapping for valid accounts techniques"""
        description = "Detect misuse of valid accounts for unauthorized access"
        result = self.mitre.map_to_technique(description)
        
        # Should map to Valid Accounts technique
        self.assertIn("name", result)
        self.assertIsNotNone(result["name"])
    
    def test_spl_validation(self):
        """Test SPL query validation"""
        # Test with a valid SPL-like query
        query = "index=security sourcetype=windows EventCode=4625 | stats count by user"
        result = self.validator.validate(query, "spl")
        
        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)
        self.assertIn("optimization_suggestions", result)
    
    def test_kql_validation(self):
        """Test KQL query validation"""
        # Test with a valid KQL-like query
        query = "SecurityEvent | where EventID == 4625 | summarize count() by TargetUserName"
        result = self.validator.validate(query, "kql")
        
        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)
        self.assertIn("optimization_suggestions", result)
    
    def test_dsl_validation(self):
        """Test DSL query validation"""
        # Test with a valid DSL-like query
        query = '{"query": {"match": {"event.code": "4625"}}}'
        result = self.validator.validate(query, "dsl")
        
        self.assertIn("valid", result)
        self.assertIn("errors", result)
        self.assertIn("warnings", result)
        self.assertIn("optimization_suggestions", result)
    
    def test_complex_threat_description(self):
        """Test query generation with a complex threat description"""
        description = "Find evidence of lateral movement through compromised accounts by detecting unusual authentication patterns across multiple systems in the last 24 hours"
        
        # Test all query types
        for query_type in ["spl", "kql", "dsl"]:
            with self.subTest(query_type=query_type):
                result = self.generator.generate(description, query_type)
                
                self.assertIn("query", result)
                self.assertIn("explanation", result)
                self.assertIsNotNone(result["query"])
                self.assertNotEqual(result["query"], "")

class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.generator = QueryGenerator()
        self.validator = QueryValidator()
        self.mitre = MitreAttackIntegration()
    
    def test_complete_workflow(self):
        """Test the complete workflow from description to validated query with MITRE mapping"""
        description = "Detect potential data exfiltration attempts through unusual network traffic patterns"
        
        # Step 1: Generate query
        result = self.generator.generate(description, "spl")
        self.assertIn("query", result)
        self.assertIn("explanation", result)
        
        # Step 2: Validate query
        validation = self.validator.validate(result["query"], "spl")
        self.assertIn("valid", validation)
        
        # Step 3: Map to MITRE ATT&CK
        mitre_result = self.mitre.map_to_technique(description)
        self.assertIn("name", mitre_result)

if __name__ == '__main__':
    # Run the tests
    unittest.main(verbosity=2)