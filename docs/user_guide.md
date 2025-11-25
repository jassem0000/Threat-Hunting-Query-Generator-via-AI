# User Guide: Threat Hunting Query Generator

## Getting Started

### Prerequisites

Before using the Threat Hunting Query Generator, ensure you have the following installed:

1. Python 3.9 or higher
2. Ollama (https://ollama.ai/)
3. At least one supported LLM model (Llama 3.2, Mistral, or Gemma 2)

### Installation

1. Download or clone the project repository
2. Install Ollama from https://ollama.ai/
3. Pull a supported model:
   ```
   ollama pull llama3.2
   ```
4. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application

1. Start the Django backend:
   ```
   cd backend
   python manage.py migrate
   python manage.py runserver
   ```
2. Start the Streamlit frontend in a new terminal:
   ```
   streamlit run frontend/app.py
   ```
3. Open your browser and navigate to http://localhost:8501

## Using the Application

### Main Interface

The application has three main tabs:

1. **Query Generator**: Main interface for generating threat hunting queries
2. **MITRE ATT&CK Mapping**: View available MITRE ATT&CK techniques
3. **About**: Project information and documentation

### Generating Queries

1. In the **Query Generator** tab, enter a natural language description of what you want to hunt for in the text area. For example:
   ```
   Find all failed login attempts from external IP addresses in the last 24 hours
   ```
2. Select your desired query type from the sidebar:
   - **Splunk SPL**: For Splunk Enterprise Security
   - **KQL**: For Microsoft Sentinel
   - **Elasticsearch DSL**: For Elastic Stack
3. Optionally enable MITRE ATT&CK mapping to get contextual threat intelligence
4. Click the "Generate Query" button

### Interpreting Results

After generating a query, you'll see:

1. **Generated Query**: The actual query code for your selected platform
2. **Explanation**: Description of what the query does and what it's looking for
3. **Validation Results**: Syntax validation and optimization suggestions
4. **MITRE ATT&CK Mapping**: Relevant attack techniques (if enabled)

## Example Use Cases

### Failed Login Detection

**Description**: "Find all failed login attempts from external IP addresses in the last 24 hours"
**Query Types**:

- SPL: `index=security sourcetype=windows EventCode=4625 | stats count by user, src_ip`
- KQL: `SecurityEvent | where EventID == 4625 | summarize count() by TargetUserName, IpAddress`
- DSL: `{"query": {"bool": {"must": [{"match": {"event.code": "4625"}}], "filter": [{"range": {"@timestamp": {"gte": "now-24h"}}}]}}}`

### PowerShell Activity Monitoring

**Description**: "Identify suspicious PowerShell activity that may indicate malicious script execution"
**Query Types**:

- SPL: `index=windows EventCode=4103 OR EventCode=4104 | search ProcessName="powershell.exe"`
- KQL: `SecurityEvent | where EventID in (4103, 4104) | where ProcessName contains "powershell"`
- DSL: `{"query": {"bool": {"should": [{"match": {"event.id": 4103}}, {"match": {"event.id": 4104}}], "must": [{"match": {"process.name": "powershell"}}]}}}`

## Troubleshooting

### Common Issues

1. **Connection Error**: Ensure the Django backend is running on http://localhost:8000
2. **LLM Not Found**: Make sure you've pulled a supported model with Ollama
3. **Empty Results**: Check that your threat description is clear and specific
4. **Validation Errors**: Review the suggested optimizations to improve query performance

### Getting Help

If you encounter issues not covered in this guide:

1. Check the console output for error messages
2. Verify all prerequisites are installed correctly
3. Ensure no firewall is blocking local connections
4. Consult the project documentation in the `docs/` directory

## Best Practices

### Writing Effective Threat Descriptions

1. Be specific about what you're looking for
2. Include timeframes when relevant
3. Mention specific event types or log sources
4. Describe the potential attack pattern

### Query Optimization

1. Always review validation suggestions
2. Add appropriate time bounds to limit search scope
3. Use indexes or specific log sources when possible
4. Test queries in your SIEM before deploying

### Security Considerations

1. All processing happens locally - no data leaves your environment
2. Regularly update your LLM models for improved accuracy
3. Review generated queries before using in production environments
4. Keep your Ollama installation up to date

## Contributing

This is an academic project, but contributions are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
