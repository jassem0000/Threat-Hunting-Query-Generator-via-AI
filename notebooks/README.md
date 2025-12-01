# Jupyter Notebooks - Threat Hunting Query Generator

This directory contains Jupyter notebooks for experimentation, model comparison, and performance analysis.

## Available Notebooks

### 1. Query Generation Examples (`01_query_generation_examples.ipynb`)

Demonstrates practical threat hunting scenarios with real-world examples.

**Features:**
- Generate queries for common threats (brute force, ransomware, data exfiltration, etc.)
- Test all query formats (SPL, KQL, DSL)
- Batch testing capabilities
- MITRE ATT&CK technique mapping
- Performance metrics collection

**Use Cases:**
- Learning how to use the system
- Testing different threat scenarios
- Validating query quality
- Building a query library

### 2. Model Comparison (`02_model_comparison.ipynb`)

Compares different LLM models for query generation performance.

**Features:**
- Compare Llama 3.2, Mistral 7B, and Gemma 2 9B
- Quality scoring and validation
- Generation time benchmarking
- Interactive visualizations (Plotly charts)
- Detailed analytics and recommendations

**Metrics Evaluated:**
- Success rate
- Generation time
- Query quality score
- Syntax correctness
- Field usage
- Time range inclusion

## Getting Started

### Prerequisites

1. **Install Jupyter**:
   ```bash
   pip install jupyter notebook jupyterlab
   ```

2. **Install Required Packages**:
   ```bash
   pip install pandas plotly numpy requests
   ```

3. **Install Ollama Models** (for model comparison):
   ```bash
   ollama pull llama3.2
   ollama pull mistral
   ollama pull gemma2:9b
   ```

4. **Start Backend API**:
   ```bash
   cd backend
   python manage.py runserver
   ```

### Running Notebooks

**Option 1: Jupyter Notebook**
```bash
jupyter notebook
```

**Option 2: JupyterLab** (recommended)
```bash
jupyter lab
```

Then navigate to the `notebooks/` directory and open any notebook.

### Executing Cells

1. Click on a cell
2. Press `Shift + Enter` to run the cell
3. Or click the "Run" button in the toolbar

## Tips for Using Notebooks

### Best Practices

1. **Run cells in order** - Each notebook is designed to be run sequentially
2. **Check backend status** - Ensure the Django backend is running before executing
3. **Monitor Ollama** - Keep Ollama running for LLM queries
4. **Save results** - Export important results to CSV for later analysis

### Customization

You can modify the notebooks to:
- Add your own test scenarios
- Change evaluation metrics
- Customize visualizations
- Test different prompt templates
- Integrate with your SIEM platforms

### Common Issues

**Issue: Connection Error**
- Solution: Ensure backend is running on `http://localhost:8000`

**Issue: Model Not Found**
- Solution: Pull the model using `ollama pull <model_name>`

**Issue: Slow Generation**
- Solution: Use a lighter model (e.g., `phi-3-mini`) or increase timeout

## Creating Your Own Notebooks

You can create new notebooks for:
- Custom threat scenarios
- Integration testing with real SIEMs
- Fine-tuning experiments
- User acceptance testing
- Performance benchmarking

### Template Structure

```python
# 1. Import dependencies
import requests
import pandas as pd
import plotly.express as px

# 2. Configure API
API_URL = "http://localhost:8000/api"

# 3. Define test scenarios
scenarios = [...]

# 4. Run experiments
results = []
for scenario in scenarios:
    result = generate_query(scenario)
    results.append(result)

# 5. Analyze and visualize
df = pd.DataFrame(results)
# Create charts and tables
```

## Exporting Results

All notebooks support exporting results:

```python
# Export to CSV
df.to_csv('results.csv', index=False)

# Export to JSON
import json
with open('results.json', 'w') as f:
    json.dump(results, f, indent=2)
```

## Integration with CI/CD

You can run notebooks automatically in CI/CD:

```bash
# Convert notebook to Python script
jupyter nbconvert --to script notebook.ipynb

# Execute with papermill
papermill input.ipynb output.ipynb -p parameter value
```

## Contributing

To add new notebooks:
1. Create a new `.ipynb` file
2. Follow the naming convention: `NN_descriptive_name.ipynb`
3. Include clear markdown documentation
4. Add sample data or use existing datasets
5. Test thoroughly before committing

## Resources

- [Jupyter Documentation](https://jupyter.org/documentation)
- [Plotly Python](https://plotly.com/python/)
- [Pandas Guide](https://pandas.pydata.org/docs/)
- [Ollama API](https://github.com/ollama/ollama/blob/main/docs/api.md)

## License

MIT License - See main project LICENSE file
