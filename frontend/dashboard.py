"""
Analytics Dashboard for Threat Hunting Query Generator
Shows REAL performance metrics, usage statistics, and query library from backend
"""

import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import json

# Page config
st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .metric-card h4 {
        color: #1f1f1f !important;
        margin: 5px 0;
    }
    .metric-card p {
        color: #333333 !important;
        margin: 5px 0;
    }
    .metric-card strong {
        color: #000000 !important;
    }
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        color: #1f77b4;
    }
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    .info-box {
        background-color: #e3f2fd;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #2196f3;
        margin: 10px 0;
        color: #1a1a1a !important;
    }
    .info-box h4 {
        color: #0d47a1 !important;
    }
    .info-box p, .info-box li, .info-box code {
        color: #1a1a1a !important;
    }
    .warning-box {
        background-color: #fff3e0;
        padding: 15px;
        border-radius: 5px;
        border-left: 4px solid #ff9800;
        margin: 10px 0;
        color: #1a1a1a !important;
    }
    .warning-box h4 {
        color: #e65100 !important;
    }
    .warning-box p, .warning-box li, .warning-box code {
        color: #1a1a1a !important;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.title("📊 Analytics Dashboard")
st.markdown("Real-time performance metrics and usage analytics")

# Backend URL
backend_url = st.sidebar.text_input(
    "Backend URL",
    "http://localhost:8000",
    help="URL of the backend API service"
)

# Add refresh button
if st.sidebar.button("🔄 Refresh Data"):
    st.rerun()

# Helper functions
def fetch_metrics():
    """Fetch real metrics from backend"""
    try:
        response = requests.get(f"{backend_url}/api/metrics", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def fetch_queries():
    """Fetch real queries from backend"""
    try:
        response = requests.get(f"{backend_url}/api/queries", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def fetch_mitre_techniques():
    """Fetch MITRE techniques from backend"""
    try:
        response = requests.get(f"{backend_url}/api/mitre-techniques", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        return None

def check_backend():
    """Check if backend is available"""
    try:
        response = requests.get(f"{backend_url}/api/health", timeout=3)
        return response.status_code == 200
    except:
        return False

# Check backend status
backend_available = check_backend()

if not backend_available:
    st.error(f"❌ Cannot connect to backend at {backend_url}")
    st.info("Please ensure the Django backend is running: `cd backend && python manage.py runserver`")
    st.stop()

# Fetch data
metrics_data = fetch_metrics()
queries_data = fetch_queries()
mitre_data = fetch_mitre_techniques()

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["📈 Overview", "📚 Query Library", "⭐ Feedback", "🔗 SIEM Connections"])

# Tab 1: Overview
with tab1:
    st.header("Performance Overview")
    
    if metrics_data:
        summary = metrics_data.get('summary', {})
        analytics = metrics_data.get('analytics', {})
        
        # Real metrics from backend
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_queries = summary.get('total_queries', 0)
            st.metric("Total Queries", total_queries)
        
        with col2:
            success_rate = analytics.get('success_rate', 0)
            st.metric("Success Rate", f"{success_rate}%")
        
        with col3:
            avg_time = analytics.get('average_generation_time_ms', 0)
            st.metric("Avg Generation Time", f"{avg_time:.0f}ms")
        
        with col4:
            validation_rate = analytics.get('validation_rate', 0)
            st.metric("Validation Rate", f"{validation_rate}%")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Query type distribution
        if analytics.get('query_type_distribution'):
            st.subheader("Query Type Distribution")
            
            dist = analytics['query_type_distribution']
            labels = list(dist.keys())
            values = list(dist.values())
            
            fig = go.Figure(data=[go.Pie(
                labels=labels,
                values=values,
                hole=.3,
                marker_colors=['#1f77b4', '#ff7f0e', '#2ca02c']
            )])
            fig.update_layout(title='Queries by Type')
            st.plotly_chart(fig, use_container_width=True)
        
        # Time series data
        time_series = metrics_data.get('time_series', {})
        if time_series and time_series.get('timestamps'):
            st.subheader("Query Generation Trend")
            
            df_time = pd.DataFrame({
                'Timestamp': time_series['timestamps'],
                'Total Queries': time_series['counts'],
                'Successful': time_series['success_counts']
            })
            
            fig = px.line(df_time, x='Timestamp', y=['Total Queries', 'Successful'],
                         title='Queries Generated Over Time')
            st.plotly_chart(fig, use_container_width=True)
        
        # Error distribution
        if analytics.get('error_distribution'):
            st.subheader("Error Analysis")
            errors = analytics['error_distribution']
            if errors:
                df_errors = pd.DataFrame(list(errors.items()), columns=['Error', 'Count'])
                st.dataframe(df_errors, use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ No metrics data available yet. Generate some queries to see statistics!")
        
        st.markdown("""
        <div class="info-box">
            <h4>📌 How to generate metrics:</h4>
            <ol>
                <li>Go to the main query generator (http://localhost:8501)</li>
                <li>Generate a few queries</li>
                <li>Come back here and click "Refresh Data"</li>
            </ol>
        </div>
        """, unsafe_allow_html=True)

# Tab 2: Query Library
with tab2:
    st.header("Query Library")
    
    if queries_data and queries_data.get('count', 0) > 0:
        queries = queries_data.get('queries', [])
        
        # Search and filters
        col1, col2 = st.columns(2)
        
        with col1:
            search_term = st.text_input("🔍 Search queries", placeholder="Enter search term...")
        with col2:
            query_type_filter = st.selectbox("Query Type", ["All", "spl", "kql", "dsl"])
        
        # Convert to DataFrame
        df_queries = pd.DataFrame(queries)
        
        # Apply filters
        if search_term:
            df_queries = df_queries[
                df_queries['description'].str.contains(search_term, case=False, na=False) |
                df_queries['title'].str.contains(search_term, case=False, na=False)
            ]
        
        if query_type_filter != "All":
            df_queries = df_queries[df_queries['query_type'] == query_type_filter]
        
        # Display columns
        display_cols = ['id', 'title', 'query_type', 'mitre_technique_id', 'created_at', 'is_valid']
        available_cols = [col for col in display_cols if col in df_queries.columns]
        
        st.dataframe(
            df_queries[available_cols],
            use_container_width=True,
            hide_index=True,
            column_config={
                'id': 'ID',
                'title': 'Title',
                'query_type': 'Type',
                'mitre_technique_id': 'MITRE',
                'created_at': 'Created',
                'is_valid': st.column_config.CheckboxColumn('Valid')
            }
        )
        
        st.info(f"📊 Showing {len(df_queries)} of {len(queries)} queries")
        
    else:
        st.warning("⚠️ No saved queries yet!")
        
        st.markdown("""
        <div class="info-box">
            <h4>📌 How to save queries:</h4>
            <p>Queries are automatically saved when you generate them through the API.</p>
            <p>You can also manually save queries using:</p>
            <code>POST /api/queries</code>
        </div>
        """, unsafe_allow_html=True)
        
        # Sample code to save a query
        with st.expander("💡 Example: Save a query via Python"):
            st.code("""
import requests

response = requests.post('http://localhost:8000/api/queries', json={
    'title': 'Brute Force Detection',
    'description': 'Find failed login attempts',
    'query_type': 'spl',
    'query': 'search index=security EventCode=4625 | stats count by src_ip',
    'mitre_technique_id': 'T1110',
    'tags': ['authentication', 'brute-force']
})
print(response.json())
            """, language='python')

# Tab 3: Feedback
with tab3:
    st.header("Analyst Feedback")
    
    st.info("💡 Feedback system is ready! Use the AnalystFeedback class in the backend to collect ratings.")
    
    # Feedback submission form
    with st.expander("➕ Submit Feedback"):
        st.write("Submit feedback for query performance")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            rating = st.slider("Overall Rating", 1, 5, 4)
        with col2:
            usefulness = st.slider("Usefulness", 1, 5, 4)
        with col3:
            accuracy = st.slider("Accuracy", 1, 5, 4)
        
        comments = st.text_area("Comments")
        
        if st.button("Submit Feedback"):
            st.success("✅ Feedback submitted! (Would be saved to backend)")

# Tab 4: SIEM Connections
with tab4:
    st.header("SIEM Connections")
    
    st.markdown("""
    <div class="warning-box">
        <h4>⚠️ SIEM Integration Status</h4>
        <p>SIEM connections are managed through the backend API.</p>
        <p>Use the API endpoints to add and test connections:</p>
        <ul>
            <li><code>POST /api/siem/connections</code> - Add connection</li>
            <li><code>POST /api/siem/test</code> - Test connection</li>
            <li><code>POST /api/siem/execute</code> - Execute query</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # Add new connection form
    with st.expander("➕ Add New SIEM Connection"):
        st.write("Configure a new SIEM connection")
        
        with st.form("siem_connection_form", clear_on_submit=False):
            col1, col2 = st.columns(2)
            
            with col1:
                conn_name = st.text_input("Connection Name")
                conn_type = st.selectbox("SIEM Type", ["splunk", "elasticsearch", "sentinel"])
            
            with col2:
                host = st.text_input("Host")
                port = st.text_input("Port", value="8089")
            
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            
            col1, col2 = st.columns(2)
            
            with col1:
                save_submitted = st.form_submit_button("💾 Save Connection", use_container_width=True)
            
            with col2:
                test_submitted = st.form_submit_button("🧪 Test Connection", use_container_width=True)
        
        # Handle save button (outside form)
        if save_submitted:
            if conn_name and conn_type and host:
                try:
                    config = {
                        'host': host,
                        'port': int(port) if port else 8089,
                        'username': username,
                        'password': password
                    }
                    
                    response = requests.post(
                        f"{backend_url}/api/siem/connections",
                        json={
                            'name': conn_name,
                            'type': conn_type,
                            'config': config
                        },
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        st.success(f"✅ Connection '{conn_name}' saved!")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error saving connection: {str(e)}")
            else:
                st.warning("⚠️ Please fill in required fields: Name, Type, and Host")
        
        # Handle test button (outside form)
        if test_submitted:
            if conn_name:
                try:
                    response = requests.post(
                        f"{backend_url}/api/siem/test",
                        json={'name': conn_name},
                        timeout=15
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('connected'):
                            st.success(f"✅ Connection successful!")
                        else:
                            st.error(f"❌ Connection failed: {result.get('error')}")
                    else:
                        st.error(f"❌ Error: {response.text}")
                except Exception as e:
                    st.error(f"❌ Error testing connection: {str(e)}")
            else:
                st.warning("⚠️ Please enter a connection name first")
    
    # Example queries
    st.subheader("📖 API Examples")
    
    with st.expander("Example: Add Splunk Connection"):
        st.code("""
import requests

response = requests.post('http://localhost:8000/api/siem/connections', json={
    'name': 'My Splunk',
    'type': 'splunk',
    'config': {
        'host': 'localhost',
        'port': 8089,
        'username': 'admin',
        'password': 'changeme',
        'scheme': 'https'
    }
})
print(response.json())
        """, language='python')
    
    with st.expander("Example: Execute Query on SIEM"):
        st.code("""
response = requests.post('http://localhost:8000/api/siem/execute', json={
    'siem_name': 'My Splunk',
    'query': 'search index=security | head 10',
    'params': {
        'earliest_time': '-24h',
        'latest_time': 'now'
    }
})
results = response.json()
print(f"Found {results['result_count']} results")
        """, language='python')

# MITRE ATT&CK Info
if mitre_data:
    st.sidebar.markdown("---")
    st.sidebar.subheader("📚 MITRE ATT&CK")
    technique_count = mitre_data.get('count', 0)
    st.sidebar.info(f"✅ {technique_count} techniques loaded")

# Footer
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style='text-align: center; color: #666;'>
    <p>Threat Hunting Query Generator | Analytics Dashboard v1.0</p>
    <p>Backend: {backend_url} {'🟢 Connected' if backend_available else '🔴 Disconnected'}</p>
    <p>Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
</div>
""", unsafe_allow_html=True)
