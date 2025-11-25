# Threat-Hunting Query Generator via AI

An AI system that automatically generates threat-hunting queries (Splunk SPL, Elasticsearch DSL, KQL) from natural language descriptions using local LLMs.

## Features

- Natural language to threat-hunting query conversion
- Support for SPL, KQL, and Elasticsearch DSL formats
- Integration with MITRE ATT&CK framework
- Local LLM processing with Ollama
- Query validation and optimization
- Web interface for easy interaction

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
└── README.md          # Project overview and setup instructions
```

## Getting Started

### Prerequisites

1. Install Ollama from https://ollama.ai/
2. Pull a supported model: `ollama pull llama3.2`
3. Python 3.9 or higher

### Installation

You can install dependencies using one of these methods:

**Method 1: Automatic Installation**

```bash
# On Windows
install_deps.bat

# On Linux/Mac
python install_deps.py
```

**Method 2: Manual Installation**

```bash
pip install -r requirements.txt
```

**Method 3: Individual Package Installation (if conflicts occur)**

```bash
python install_deps.py
```

### Running the Application

1. Run Django migrations: `cd backend && python manage.py migrate`
2. Create a superuser (optional): `cd backend && python manage.py createsuperuser`
3. Run the backend: `cd backend && python manage.py runserver`
4. Run the frontend: `streamlit run frontend/app.py`

### Using the Run Scripts

- **Windows**: Double-click `run_project.bat`
- **Linux/Mac**: Run `./run_project.sh`

## Running Tests

The project includes several test suites to verify functionality:

### 1. Basic Functionality Test

```bash
python tests/test_query_generation.py
```

### 2. Comprehensive Unit Tests

```bash
python -m unittest tests.test_threat_hunter -v
```

### 3. Practical Examples

```bash
python tests/practical_example.py
```

### 4. All Tests Runner

```bash
python run_tests.py
```

## API Endpoints

- `POST /api/generate-query` - Generate a threat hunting query
- `GET /api/mitre-techniques` - Get all MITRE ATT&CK techniques
- `GET /api/health` - Health check endpoint

## Troubleshooting

If you encounter dependency conflicts or installation issues, refer to the [Troubleshooting Guide](docs/troubleshooting.md).

## Architecture

![Architecture Diagram](docs/architecture.png)

## License

MIT
