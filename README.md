# Threat-Hunting Query Generator via AI

An AI system that automatically generates threat-hunting queries (Splunk SPL, Elasticsearch DSL, KQL) from natural language descriptions using local LLMs.

## Features

### Core Features
- ✅ Natural language to threat-hunting query conversion
- ✅ Support for SPL, KQL, and Elasticsearch DSL formats
- ✅ Local LLM processing with Ollama (privacy-preserving)
- ✅ Query validation and optimization
- ✅ Web interface for easy interaction

### NEW: Advanced Features 🆕
- ✨ **SIEM Integration** - Direct connection to Splunk, Elasticsearch, and Azure Sentinel
- ✨ **Performance Metrics** - Comprehensive tracking of query accuracy, generation time, and analyst satisfaction
- ✨ **Full MITRE ATT&CK Framework** - 50+ techniques across all 12 tactics (vs. previous 5 techniques)
- ✨ **Query Library Management** - Save, organize, and share queries with team
- ✨ **Analytics Dashboard** - Visual dashboards with Plotly for metrics and insights
- ✨ **Jupyter Notebooks** - Reproducible experiments and model comparison
- ✨ **Query Execution** - Test generated queries on real SIEM platforms
- ✨ **Multi-Model Support** - Compare Llama 3.2, Mistral 7B, and Gemma 2 9B

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

### Core Endpoints
- `POST /api/generate-query` - Generate a threat hunting query
- `GET /api/mitre-techniques` - Get all MITRE ATT&CK techniques (50+)
- `GET /api/health` - Health check endpoint

### NEW: Advanced Endpoints 🆕
- `GET /api/metrics` - Get performance metrics and analytics
- `GET /api/queries` - List saved queries from library
- `POST /api/queries` - Save a new query to library
- `POST /api/siem/connections` - Add SIEM connection
- `POST /api/siem/test` - Test SIEM connection
- `POST /api/siem/execute` - Execute query on SIEM platform

## New Features Documentation

📖 **[Quick Start Guide](QUICK_START.md)** - Get started with all new features  
📊 **[Completion Report](COMPLETION_REPORT.md)** - Detailed report on all improvements  
📓 **[Jupyter Notebooks](notebooks/README.md)** - Reproducible experiments and model comparison  
🎯 **[Implementation Analysis](IMPLEMENTATION_ANALYSIS.md)** - Technical implementation details  

## Troubleshooting

If you encounter dependency conflicts or installation issues, refer to the [Troubleshooting Guide](docs/troubleshooting.md).

## What's New in v1.0

### 🚀 Major Enhancements

1. **SIEM Integration** - Connect to Splunk, Elasticsearch, and Azure Sentinel
2. **Performance Tracking** - Automatic metrics collection and analytics
3. **Enhanced MITRE Coverage** - Expanded from 5 to 50+ techniques
4. **Query Library** - Save, organize, and manage queries
5. **Analytics Dashboard** - New Streamlit dashboard for visualization
6. **Jupyter Notebooks** - Two comprehensive notebooks for experiments

See [COMPLETION_REPORT.md](COMPLETION_REPORT.md) for full details.

## Architecture

![Architecture Diagram](docs/architecture.png)

## Screenshots

### Main Query Generator
Generate queries from natural language with MITRE ATT&CK mapping.

### Analytics Dashboard 🆕
Visual metrics, query library, and SIEM connection management.

### Jupyter Notebooks 🆕
Reproducible experiments and model comparison.

## License

MIT
