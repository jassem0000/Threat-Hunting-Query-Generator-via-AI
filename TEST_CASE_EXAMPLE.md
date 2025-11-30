# Test Case Example for Threat Hunting Query Generator

This document provides a detailed example of how to create and run a test case for the Threat Hunting Query Generator.

## Sample Test Case: Detecting Brute Force Attacks

### Test Description

We want to test the system's ability to generate queries that detect brute force attacks against SSH services.

### Input

**Threat Description**: "Detect brute force attacks against SSH services by identifying hosts with more than 10 failed login attempts in the last hour"

### Expected Output

1. **SPL Query**: Should contain elements for counting failed SSH login attempts
2. **KQL Query**: Should filter SecurityEvent logs for SSH-related events
3. **DSL Query**: Should search for authentication failure patterns
4. **MITRE Mapping**: Should map to T1110 - Brute Force
5. **Validation**: Should pass basic syntax checks

### Implementation

```python
# Test case implementation
def test_ssh_brute_force_detection(self):
    """Test SSH brute force detection query generation"""
    description = "Detect brute force attacks against SSH services by identifying hosts with more than 10 failed login attempts in the last hour"

    # Test SPL generation
    spl_result = self.generator.generate(description, "spl")
    self.assertIn("ssh", spl_result["query"].lower())
    self.assertIn("count", spl_result["query"].lower())

    # Test KQL generation
    kql_result = self.generator.generate(description, "kql")
    self.assertIn("SecurityEvent", kql_result["query"])

    # Test DSL generation
    dsl_result = self.generator.generate(description, "dsl")
    self.assertIn("query", dsl_result["query"])

    # Test MITRE mapping
    mitre_result = self.mitre.map_to_technique(description)
    self.assertEqual(mitre_result["technique_id"], "T1110")

    # Test validation
    spl_validation = self.validator.validate(spl_result["query"], "spl")
    self.assertTrue(spl_validation["valid"])
```

### Running the Test

1. **Setup**: Ensure all dependencies are installed and Ollama is running
2. **Execution**: Run the test using Python unittest framework
   ```bash
   python -m unittest tests.test_threat_hunter.TestQueryGenerator.test_ssh_brute_force_detection -v
   ```
3. **Verification**: Check that all assertions pass

### Expected Results

When this test runs successfully, you should see output similar to:

```
test_ssh_brute_force_detection (__main__.TestQueryGenerator) ... ok

----------------------------------------------------------------------
Ran 1 test in 2.345s

OK
```

### Sample Generated Queries

After running the test, you might see generated queries like:

**SPL**:

```
index=security sourcetype=linux_secure ssh | stats count by host, src_ip | where count > 10
```

**KQL**:

```
SecurityEvent | where EventID == 4625 | summarize count() by TargetUserName, IpAddress | where count_ > 10
```

**DSL**:

```json
{
  "query": {
    "bool": {
      "must": [
        { "match": { "event.code": "4625" } },
        { "range": { "@timestamp": { "gte": "now-1h" } } }
      ]
    }
  }
}
```

### Test Coverage

This single test case covers:

- [x] Query generation functionality
- [x] Multiple query format support
- [x] MITRE ATT&CK integration
- [x] Query validation
- [x] Error handling (implicit)
- [x] Component integration

### Extending the Test

To create more comprehensive tests, you could:

1. **Add negative test cases**:

   ```python
   def test_invalid_query_type(self):
       with self.assertRaises(ValueError):
           self.generator.generate("test", "invalid_type")
   ```

2. **Add performance tests**:

   ```python
   import time

   def test_query_generation_performance(self):
       start_time = time.time()
       self.generator.generate("test description", "spl")
       end_time = time.time()
       self.assertLess(end_time - start_time, 5.0)  # Should complete in < 5 seconds
   ```

3. **Add data-driven tests**:
   ```python
   def test_multiple_threat_scenarios(self):
       test_cases = [
           ("Detect malware execution", "T1059"),
           ("Find data exfiltration", "T1041"),
           ("Identify privilege escalation", "T1068")
       ]

       for description, expected_technique in test_cases:
           with self.subTest(description=description):
               result = self.mitre.map_to_technique(description)
               self.assertIn(expected_technique, result["technique_id"])
   ```

This test case example demonstrates the core functionality of the Threat Hunting Query Generator and shows how to properly test each component of the system.
