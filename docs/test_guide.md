# Test Guide for Threat Hunting Query Generator

This guide explains how to run tests for the Threat Hunting Query Generator project.

## Test Suite Overview

The project includes several test suites to verify functionality:

1. **Basic Functionality Test** - Simple smoke test to verify core components
2. **Comprehensive Unit Tests** - Full test coverage of all components
3. **Practical Examples** - Real-world usage scenarios
4. **Edge Case Tests** - Boundary condition and error handling tests

## Prerequisites

Before running tests, ensure you have:

1. Installed all project dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Ollama service running with a supported model:
   ```bash
   ollama pull llama3.1
   ```

## Running Tests

### 1. Basic Functionality Test

This test verifies that the core components can be imported and instantiated:

```bash
python tests/test_query_generation.py
```

Expected output:

- Successful instantiation of QueryGenerator, QueryValidator, and MitreAttackIntegration
- Query generation for sample threat descriptions
- Basic validation of generated queries

### 2. Comprehensive Unit Tests

This test suite provides full coverage of all components:

```bash
python -m unittest tests.test_threat_hunter -v
```

Tests include:

- Component initialization
- Query generation for all supported formats (SPL, KQL, DSL)
- MITRE ATT&CK technique mapping
- Query validation and optimization
- Error handling for invalid inputs
- Integration testing of complete workflow

### 3. Practical Examples

This demonstrates real-world usage scenarios:

```bash
python tests/practical_example.py
```

Features:

- Real-world threat hunting scenarios
- Interactive mode for custom descriptions
- Detailed output with explanations
- MITRE ATT&CK mapping for each scenario

### 4. Simple Edge Case Tests

This tests boundary conditions and error handling:

```bash
python tests/simple_edge_tests.py
```

Tests include:

- Empty descriptions
- Invalid query types
- None and empty string inputs
- Special characters in descriptions

### 5. All Tests Runner

Run all tests at once:

```bash
python run_tests.py
```

## Test Case Examples

### Sample Test Case 1: Brute Force Detection

**Description**: "Find all failed login attempts from external IP addresses in the last 24 hours"
**Expected Output**:

- SPL query with index, sourcetype, and EventCode filters
- KQL query with SecurityEvent and EventID filters
- DSL query with match and range clauses

### Sample Test Case 2: PowerShell Activity

**Description**: "Identify suspicious PowerShell activity that may indicate malicious script execution"
**Expected Output**:

- SPL query with PowerShell event codes (4103, 4104)
- KQL query with ProcessName containing "powershell"
- DSL query with process name matching

### Sample Test Case 3: Data Exfiltration

**Description**: "Detect potential data exfiltration attempts through unusual network traffic patterns"
**Expected Output**:

- SPL query with network traffic analysis
- KQL query with outbound traffic filtering
- DSL query with byte transfer analysis

## Expected Test Results

### Successful Tests

- All components initialize without errors
- Queries are generated for all supported formats
- Generated queries pass basic validation
- MITRE ATT&CK mapping returns relevant techniques
- Error handling works for invalid inputs

### Known Limitations

- Query generation quality depends on LLM capabilities
- MITRE mapping uses simple keyword matching
- Validation provides basic syntax checking only
- Some edge cases may not be fully handled

## Troubleshooting Test Issues

### ImportError Messages

If you see import errors, ensure:

1. You're running tests from the project root directory
2. All dependencies are installed
3. Python path includes the backend directory

### Ollama Connection Errors

If query generation fails:

1. Ensure Ollama service is running
2. Verify a supported model is installed
3. Check that http://localhost:11434 is accessible

### Test Failures

If specific tests fail:

1. Check the error message for details
2. Verify the test case expectations match implementation
3. Update tests if functionality has changed

## Adding New Tests

To add new test cases:

1. Create a new method in `tests/test_threat_hunter.py`
2. Follow the naming convention `test_descriptive_name`
3. Use assertions to verify expected behavior
4. Run tests to ensure they pass

Example:

```python
def test_custom_threat_scenario(self):
    """Test custom threat hunting scenario"""
    description = "Custom threat description"
    result = self.generator.generate(description, "spl")
    self.assertIn("expected_element", result["query"])
```

## Continuous Integration

For CI/CD pipelines, use:

```bash
python -m unittest discover tests -v
```

This will discover and run all test files in the tests directory.
