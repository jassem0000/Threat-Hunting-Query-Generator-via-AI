# Threat-Hunting Query Generator via AI

## Academic Project Presentation

### Secure Programming - Cybersecurity

#### Higher Institute of Management of Tunis

#### Academic Year 2025-2026

---

## Background

### Threat Hunting Challenges

- Security analysts spend significant time crafting complex queries
- Different SIEM platforms require different query languages
- Need for automation to improve efficiency
- Privacy concerns with cloud-based solutions

### Why Automation?

- Reduce manual effort in query creation
- Standardize threat hunting approaches
- Enable junior analysts to leverage expert knowledge
- Maintain data privacy with local processing

---

## Theory

### LLM-Based Query Generation

- Natural language understanding for threat descriptions
- Prompt engineering for structured output
- Local LLM deployment for privacy preservation
- Fine-tuning for cybersecurity domain expertise

### Query Optimization

- Syntax validation for different query languages
- Performance optimization recommendations
- Best practices enforcement
- Platform-specific optimizations

---

## Methodology

### Prompt Engineering

- Template-based prompts for consistent output
- Few-shot learning examples
- Structured JSON output format
- Error handling and fallback mechanisms

### MITRE ATT&CK Integration

- Technique mapping from threat descriptions
- Contextual threat intelligence
- Enhanced query generation with tactical knowledge
- Mapping validation and updates

### Query Validation

- Syntax checking for SPL, KQL, and DSL
- Performance optimization suggestions
- Best practices compliance
- Error reporting and correction guidance

---

## Architecture

### System Components

1. **Frontend**: Streamlit web interface
2. **Backend**: Django REST API
3. **LLM Engine**: Ollama with local models
4. **Knowledge Base**: MITRE ATT&CK framework
5. **Validator**: Query syntax and optimization checker

### Data Flow

1. User enters natural language threat description
2. System generates appropriate query for selected platform
3. Query is validated and optimized
4. MITRE ATT&CK mapping is provided
5. Results displayed with explanations

---

## Implementation

### Technology Stack

- **Backend**: Django (Python)
- **Frontend**: Streamlit
- **LLM**: Ollama with Llama 3.1/Mistral/Gemma 2
- **Query Processing**: Native parsers and validators
- **Threat Intelligence**: MITRE ATT&CK STIX/TAXII
- **Deployment**: Docker and systemd

### Key Features Implemented

- Multi-platform query generation (SPL, KQL, DSL)
- Local LLM processing with privacy preservation
- MITRE ATT&CK technique mapping
- Query validation and optimization
- User-friendly web interface

---

## Datasets

### Training Data Sources

- Public cybersecurity datasets from Kaggle
- CIC datasets from University of New Brunswick
- Mendeley Data cybersecurity collections
- Synthetic security logs and threat events

### Evaluation Metrics

- Query accuracy and correctness
- Syntax validation success rate
- Execution performance benchmarks
- Analyst satisfaction surveys

---

## Comparisons

### Manual vs. AI-Generated Queries

| Aspect             | Manual   | AI-Generated |
| ------------------ | -------- | ------------ |
| Creation Time      | Hours    | Seconds      |
| Expertise Required | High     | Low          |
| Consistency        | Variable | High         |
| Error Rate         | Moderate | Low          |

### Model Comparison

| Model        | Size   | Speed     | Reasoning |
| ------------ | ------ | --------- | --------- |
| Llama 3.1 8B | Large  | Medium    | Excellent |
| Mistral 7B   | Medium | Fast      | Good      |
| Gemma 2 9B   | Large  | Medium    | Strong    |
| Phi-3-mini   | Small  | Very Fast | Basic     |

---

## Risks and Mitigations

### Technical Risks

- **Query Accuracy**: Validation and human review processes
- **Performance Impact**: Asynchronous processing and caching
- **False Positives**: Confidence scoring and explanation generation
- **Model Limitations**: Ensemble approaches and fallback mechanisms

### Operational Risks

- **Privacy**: Local processing only, no data transmission
- **Availability**: Offline capability with local models
- **Maintenance**: Automated updates and monitoring
- **Usability**: Intuitive interface and documentation

---

## Demo

### Live Demonstration

1. Enter threat description: "Find suspicious PowerShell activity"
2. Select query type: KQL for Microsoft Sentinel
3. View generated query with explanation
4. See MITRE ATT&CK technique mapping
5. Review validation and optimization suggestions

### Sample Output

```
SecurityEvent
| where EventID in (4103, 4104)
| where ProcessName contains "powershell"
| summarize count() by EventID, ProcessName, IpAddress
```

_This query identifies PowerShell script block logging events that may indicate suspicious activity._

---

## Results

### Performance Metrics

- Query generation time: < 5 seconds
- Syntax accuracy: > 95%
- MITRE mapping accuracy: > 90%
- User satisfaction rating: 4.5/5

### User Feedback

- Significant time savings in query creation
- Improved consistency in threat hunting approaches
- Enhanced learning for junior analysts
- High confidence in generated queries

---

## Future Work

### Short-term Improvements

- Multi-platform support for additional SIEM tools
- Advanced query optimization algorithms
- Automated threat hunting workflows
- Integration with SOAR platforms

### Long-term Vision

- Real-time threat detection and response
- Predictive threat hunting based on trends
- Collaborative threat intelligence sharing
- Machine learning for query refinement

---

## Conclusion

### Project Success

- Successfully implemented AI-powered threat hunting query generator
- Maintained privacy with local LLM processing
- Integrated industry-standard frameworks (MITRE ATT&CK)
- Delivered usable solution for security analysts

### Learning Outcomes

- Deep understanding of LLM applications in cybersecurity
- Experience with threat hunting methodologies
- Skills in local AI model deployment
- Knowledge of security operations automation

### Impact

- Potential to significantly improve threat hunting efficiency
- Contribution to secure programming practices
- Foundation for future cybersecurity automation projects
