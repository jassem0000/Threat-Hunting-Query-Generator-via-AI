# Threat-Hunting Query Generator via AI - Project Summary

## Project Overview

This project implements an AI-powered system that automatically generates threat-hunting queries (Splunk SPL, Elasticsearch DSL, KQL) from natural language descriptions using local LLMs. The system provides security analysts with an efficient way to convert threat descriptions into actionable queries while maintaining data privacy through local processing.

## Key Features Implemented

1. **Multi-Platform Query Generation**

   - Support for Splunk SPL, KQL (Microsoft Sentinel), and Elasticsearch DSL
   - Template-based prompt engineering for consistent LLM output
   - Structured JSON response parsing

2. **Local LLM Integration**

   - Ollama integration for privacy-preserving query generation
   - Support for Llama 3.2, Mistral, and Gemma 2 models
   - Fallback mechanisms for API connectivity

3. **MITRE ATT&CK Framework Integration**

   - Technique mapping from threat descriptions
   - Contextual threat intelligence enhancement
   - Technique database with common attack patterns

4. **Query Validation and Optimization**

   - Syntax validation for all supported query languages
   - Performance optimization suggestions
   - Best practices enforcement

5. **User Interface**
   - Streamlit-based web interface for easy interaction
   - Real-time query generation and validation
   - MITRE ATT&CK technique mapping display

## Technology Stack

- **Backend**: Django (Python) with REST API
- **Frontend**: Streamlit web interface
- **AI Engine**: Ollama with local LLM models
- **Data Processing**: Native Python parsers and validators
- **Threat Intelligence**: MITRE ATT&CK framework integration
- **Deployment**: Docker and traditional installation options

## Project Structure

```
threat-hunting-ai/
├── backend/           # Django backend service
│   ├── threat_hunter/ # Django project settings
│   ├── api/           # API endpoints and business logic
│   └── manage.py      # Django management script
├── frontend/          # Streamlit frontend interface
├── docs/              # Documentation and presentation materials
├── datasets/          # Sample datasets and threat intelligence
├── tests/             # Unit and integration tests
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker image definition
├── docker-compose.yml # Multi-container deployment
└── README.md          # Project overview and setup instructions
```

## Implementation Details

### Backend (Django)

- REST API endpoints for query generation and validation
- Modular architecture with separate components for each functionality
- Error handling and fallback mechanisms
- Health check and monitoring endpoints

### Query Generation

- Prompt engineering for different query languages
- LLM response parsing and validation
- Fallback mechanisms for API failures
- Structured output formatting

### MITRE ATT&CK Integration

- Technique mapping based on keyword matching
- Technique database with descriptions
- API endpoint for technique retrieval

### Validation System

- Language-specific syntax validators
- Performance optimization suggestions
- Best practices checking
- Detailed error reporting

### Frontend (Streamlit)

- Intuitive user interface for threat description input
- Real-time query generation and display
- Validation results visualization
- MITRE ATT&CK technique mapping

## How to Run the Project

### Prerequisites

1. Python 3.9+
2. Ollama (https://ollama.ai/)
3. At least one supported LLM model (Llama 3.2, Mistral, or Gemma 2)

### Installation Steps

1. Install Ollama from https://ollama.ai/
2. Pull a supported model: `ollama pull llama3.2`
3. Install Python dependencies: `pip install -r requirements.txt`
4. Run Django migrations: `cd backend && python manage.py migrate`
5. Start the backend: `cd backend && python manage.py runserver`
6. Start the frontend: `streamlit run frontend/app.py`

### Docker Deployment

1. Build and run with Docker Compose: `docker-compose up`
2. Access the frontend at http://localhost:8501
3. Backend API available at http://localhost:8000

## Academic Relevance

This project addresses key concepts from the Secure Programming curriculum:

- **Threat hunting**: Automated generation of hunting queries
- **Query generation**: NLP to structured query conversion
- **Local LLMs**: Privacy-preserving AI processing
- **MITRE ATT&CK**: Industry-standard threat framework integration
- **Natural language to query**: AI-powered translation
- **Security operations**: SOAR automation principles
- **Query optimization**: Performance and best practices

## Future Enhancements

1. **Advanced NLP**: More sophisticated threat description understanding
2. **Extended Platform Support**: Additional SIEM platforms
3. **Machine Learning**: Query refinement based on feedback
4. **Collaborative Features**: Team-based threat hunting workflows
5. **Automated Scheduling**: Periodic threat hunting execution
6. **Integration APIs**: Direct SIEM platform connections
7. **Advanced Visualization**: Dashboards and analytics

## Conclusion

The Threat-Hunting Query Generator successfully demonstrates the application of AI in cybersecurity operations. By combining local LLM processing with industry-standard frameworks like MITRE ATT&CK, the system provides security analysts with a powerful tool for efficient threat hunting while maintaining data privacy. The modular architecture allows for easy extension and customization for different organizational needs.
