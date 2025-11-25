import streamlit as st
import requests
import json

# Set page configuration
st.set_page_config(
    page_title="Threat Hunting Query Generator",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'generated_query' not in st.session_state:
    st.session_state.generated_query = ""
if 'explanation' not in st.session_state:
    st.session_state.explanation = ""
if 'mitre_technique' not in st.session_state:
    st.session_state.mitre_technique = {}
if 'validation_result' not in st.session_state:
    st.session_state.validation_result = {}

# Custom CSS for better UI
st.markdown("""
<style>
    .stTextArea textarea {
        font-family: monospace;
        font-size: 14px;
    }
    .query-container {
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 15px;
        margin: 10px 0;
    }
    .explanation-container {
        background-color: #e8f4f8;
        border-left: 5px solid #2196f3;
        padding: 15px;
        margin: 10px 0;
    }
    .validation-container {
        background-color: #fff3e0;
        border-left: 5px solid #ff9800;
        padding: 15px;
        margin: 10px 0;
    }
    .success {
        color: #4caf50;
        font-weight: bold;
    }
    .error {
        color: #f44336;
        font-weight: bold;
    }
    .warning {
        color: #ff9800;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# App title and description
st.title("🔍 Threat Hunting Query Generator")
st.markdown("""
This tool uses AI to convert natural language descriptions into threat hunting queries for various security platforms.
Simply describe what you're looking for, and the system will generate optimized queries in SPL, KQL, or Elasticsearch DSL formats.
""")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Query Generator", "MITRE ATT&CK Mapping", "About"])

with tab1:
    # Sidebar for configuration
    st.sidebar.header("Configuration")
    
    # Backend URL input
    backend_url = st.sidebar.text_input(
        "Backend URL",
        "http://localhost:8000",
        help="URL of the backend API service"
    )
    
    # Query type selection
    query_type = st.sidebar.selectbox(
        "Query Type",
        ["spl", "kql", "dsl"],
        format_func=lambda x: {
            "spl": "Splunk SPL",
            "kql": "Kusto Query Language (KQL)",
            "dsl": "Elasticsearch DSL"
        }[x],
        help="Select the type of query to generate"
    )
    
    # MITRE ATT&CK integration option
    include_mitre = st.sidebar.checkbox(
        "Include MITRE ATT&CK Mapping",
        True,
        help="Map the query to relevant MITRE ATT&CK techniques"
    )
    
    # Main content area
    st.header("Describe Your Threat Hunt")
    
    # Text area for threat description
    threat_description = st.text_area(
        "Enter a natural language description of what you want to hunt for:",
        height=150,
        placeholder="Example: Find all failed login attempts from external IP addresses in the last 24 hours...",
        key="threat_desc"
    )
    
    # Generate button
    if st.button("Generate Query", type="primary", use_container_width=True):
        if threat_description.strip():
            try:
                # Prepare the request
                payload = {
                    "description": threat_description,
                    "query_type": query_type,
                    "include_mitre": include_mitre
                }
                
                # Make API request
                response = requests.post(
                    f"{backend_url}/api/generate-query",
                    json=payload,
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Store in session state
                    st.session_state.generated_query = data.get("query", "")
                    st.session_state.explanation = data.get("explanation", "")
                    st.session_state.mitre_technique = data.get("mitre_technique", {})
                    st.session_state.validation_result = data.get("validation_result", {})
                    
                    # Show success message
                    st.success("Query generated successfully!")
                else:
                    st.error(f"API Error: {response.status_code} - {response.text}")
                    
            except requests.exceptions.ConnectionError:
                st.error("Could not connect to the backend service. Please ensure the API is running.")
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter a threat description first.")
    
    # Display results
    if st.session_state.generated_query:
        st.subheader("Generated Query")
        st.markdown(f"<div class='query-container'><pre>{st.session_state.generated_query}</pre></div>", unsafe_allow_html=True)
        
        if st.session_state.explanation:
            st.subheader("Explanation")
            st.markdown(f"<div class='explanation-container'>{st.session_state.explanation}</div>", unsafe_allow_html=True)
        
        # Validation results
        if st.session_state.validation_result:
            st.subheader("Validation Results")
            validation = st.session_state.validation_result
            
            # Validity indicator
            if validation.get("valid"):
                st.markdown("<span class='success'>✅ Query is valid</span>", unsafe_allow_html=True)
            else:
                st.markdown("<span class='error'>❌ Query has validation errors</span>", unsafe_allow_html=True)
            
            # Errors
            errors = validation.get("errors", [])
            if errors:
                st.markdown("**Errors:**")
                for error in errors:
                    st.markdown(f"<span class='error'>• {error}</span>", unsafe_allow_html=True)
            
            # Warnings
            warnings = validation.get("warnings", [])
            if warnings:
                st.markdown("**Warnings:**")
                for warning in warnings:
                    st.markdown(f"<span class='warning'>• {warning}</span>", unsafe_allow_html=True)
            
            # Optimization suggestions
            suggestions = validation.get("optimization_suggestions", [])
            if suggestions:
                st.markdown("**Optimization Suggestions:**")
                for suggestion in suggestions:
                    st.markdown(f"💡 {suggestion}")

with tab2:
    st.header("MITRE ATT&CK Techniques")
    
    if st.button("Load MITRE ATT&CK Techniques"):
        try:
            response = requests.get(f"{backend_url}/api/mitre-techniques", timeout=10)
            if response.status_code == 200:
                data = response.json()
                techniques = data.get("techniques", [])
                
                if techniques:
                    st.subheader(f"Available Techniques ({len(techniques)})")
                    
                    # Display techniques in a table
                    for technique in techniques:
                        with st.expander(f"{technique.get('id', 'N/A')}: {technique.get('name', 'N/A')}"):
                            st.write(technique.get('description', 'No description available'))
                else:
                    st.info("No MITRE ATT&CK techniques found.")
            else:
                st.error(f"API Error: {response.status_code} - {response.text}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the backend service. Please ensure the API is running.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
    else:
        st.info("Click 'Load MITRE ATT&CK Techniques' to view available techniques.")

with tab3:
    st.header("About This Project")
    st.markdown("""
    ## Threat Hunting Query Generator via AI
    
    This project was developed as part of the Secure Programming course at the Higher Institute of Management of Tunis.
    
    ### Key Features
    - **Natural Language Processing**: Convert plain English descriptions to security queries
    - **Multi-Platform Support**: Generate queries for Splunk, Microsoft Sentinel, and Elasticsearch
    - **MITRE ATT&CK Integration**: Map threats to industry-standard frameworks
    - **Local AI Processing**: Privacy-preserving with Ollama local LLMs
    - **Query Validation**: Ensure syntactic correctness and best practices
    
    ### Technology Stack
    - **Backend**: Django (Python)
    - **Frontend**: Streamlit
    - **AI Engine**: Ollama with Llama 3.1/Mistral/Gemma 2
    - **Frameworks**: MITRE ATT&CK, STIX/TAXII
    - **Deployment**: Docker, systemd
    
    ### Academic Year 2025-2026
    """)