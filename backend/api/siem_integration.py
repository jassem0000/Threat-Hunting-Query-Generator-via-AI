"""
SIEM Integration Module
Provides connectors for Splunk, Elasticsearch, and Azure Sentinel
"""

import os
import json
from typing import Dict, Any, Optional, List
import requests
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError as ESConnectionError


class SIEMConnector:
    """Base class for SIEM connectors"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.connected = False
    
    def test_connection(self) -> Dict[str, Any]:
        """Test SIEM connection"""
        raise NotImplementedError
    
    def execute_query(self, query: str) -> Dict[str, Any]:
        """Execute a query on the SIEM"""
        raise NotImplementedError


class SplunkConnector(SIEMConnector):
    """Connector for Splunk SIEM"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.host = config.get('host', 'localhost')
        self.port = config.get('port', 8089)
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.scheme = config.get('scheme', 'https')
        self.verify_ssl = config.get('verify_ssl', False)
        self.client = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Splunk connection"""
        try:
            # Import here to avoid dependency issues if splunk-sdk not installed
            from splunklib import client
            
            self.client = client.connect(
                host=self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                scheme=self.scheme
            )
            
            # Test by getting server info
            info = self.client.info
            self.connected = True
            
            return {
                'status': 'success',
                'connected': True,
                'server_version': info.get('version', 'unknown'),
                'server_name': info.get('serverName', 'unknown')
            }
        except Exception as e:
            self.connected = False
            error_msg = str(e)
            
            # Handle common connection errors with helpful messages
            if "10061" in error_msg or "Connection refused" in error_msg:
                return {
                    'status': 'error',
                    'connected': False,
                    'error': f"Could not connect to Splunk at {self.host}:{self.port}. Is Splunk running?"
                }
            
            return {
                'status': 'error',
                'connected': False,
                'error': error_msg
            }
    
    def execute_query(self, query: str, earliest_time: str = '-24h', latest_time: str = 'now') -> Dict[str, Any]:
        """Execute a Splunk SPL query"""
        if not self.connected or not self.client:
            conn_result = self.test_connection()
            if not conn_result.get('connected'):
                return {
                    'status': 'error',
                    'error': 'Not connected to Splunk',
                    'results': []
                }
        
        try:
            from splunklib import results
            
            # Create a search job
            job = self.client.jobs.create(
                query,
                earliest_time=earliest_time,
                latest_time=latest_time
            )
            
            # Wait for the job to complete
            while not job.is_done():
                pass
            
            # Get results
            result_stream = job.results(output_mode='json')
            result_reader = results.JSONResultsReader(result_stream)
            
            query_results = []
            for result in result_reader:
                if isinstance(result, dict):
                    query_results.append(result)
            
            return {
                'status': 'success',
                'result_count': len(query_results),
                'results': query_results[:100],  # Limit to 100 results
                'scan_count': job['scanCount'],
                'event_count': job['eventCount']
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'results': []
            }


class ElasticsearchConnector(SIEMConnector):
    """Connector for Elasticsearch"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.hosts = config.get('hosts', ['localhost:9200'])
        self.username = config.get('username', '')
        self.password = config.get('password', '')
        self.use_ssl = config.get('use_ssl', False)
        self.verify_certs = config.get('verify_certs', False)
        self.client = None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Elasticsearch connection"""
        try:
            if self.username and self.password:
                self.client = Elasticsearch(
                    self.hosts,
                    http_auth=(self.username, self.password),
                    use_ssl=self.use_ssl,
                    verify_certs=self.verify_certs
                )
            else:
                self.client = Elasticsearch(
                    self.hosts,
                    use_ssl=self.use_ssl,
                    verify_certs=self.verify_certs
                )
            
            # Test connection
            info = self.client.info()
            self.connected = True
            
            return {
                'status': 'success',
                'connected': True,
                'cluster_name': info.get('cluster_name', 'unknown'),
                'version': info.get('version', {}).get('number', 'unknown')
            }
        except ESConnectionError as e:
            self.connected = False
            return {
                'status': 'error',
                'connected': False,
                'error': f'Connection error: {str(e)}'
            }
        except Exception as e:
            self.connected = False
            return {
                'status': 'error',
                'connected': False,
                'error': str(e)
            }
    
    def execute_query(self, query: str, index: str = '*', size: int = 100) -> Dict[str, Any]:
        """Execute an Elasticsearch DSL query"""
        if not self.connected or not self.client:
            conn_result = self.test_connection()
            if not conn_result.get('connected'):
                return {
                    'status': 'error',
                    'error': 'Not connected to Elasticsearch',
                    'results': []
                }
        
        try:
            # Parse query if it's a string
            if isinstance(query, str):
                query_body = json.loads(query)
            else:
                query_body = query
            
            # Execute search
            response = self.client.search(
                index=index,
                body=query_body,
                size=size
            )
            
            hits = response.get('hits', {}).get('hits', [])
            
            return {
                'status': 'success',
                'result_count': len(hits),
                'total_hits': response.get('hits', {}).get('total', {}).get('value', 0),
                'results': [hit['_source'] for hit in hits],
                'took_ms': response.get('took', 0)
            }
        except json.JSONDecodeError as e:
            return {
                'status': 'error',
                'error': f'Invalid JSON query: {str(e)}',
                'results': []
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'results': []
            }


class AzureSentinelConnector(SIEMConnector):
    """Connector for Azure Sentinel (KQL)"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.workspace_id = config.get('workspace_id', '')
        self.subscription_id = config.get('subscription_id', '')
        self.resource_group = config.get('resource_group', '')
        self.tenant_id = config.get('tenant_id', '')
        self.client_id = config.get('client_id', '')
        self.client_secret = config.get('client_secret', '')
        self.access_token = None
    
    def _get_access_token(self) -> Optional[str]:
        """Get Azure AD access token"""
        try:
            url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
            
            data = {
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'https://api.loganalytics.io/.default',
                'grant_type': 'client_credentials'
            }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                self.access_token = response.json().get('access_token')
                return self.access_token
            else:
                return None
        except Exception as e:
            print(f"Error getting access token: {e}")
            return None
    
    def test_connection(self) -> Dict[str, Any]:
        """Test Azure Sentinel connection"""
        try:
            token = self._get_access_token()
            
            if not token:
                self.connected = False
                return {
                    'status': 'error',
                    'connected': False,
                    'error': 'Failed to obtain access token'
                }
            
            # Test with a simple query
            headers = {
                'Authorization': f'Bearer {token}',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.loganalytics.io/v1/workspaces/{self.workspace_id}/query"
            
            test_query = {
                'query': 'print "test"',
                'timespan': 'PT1H'
            }
            
            response = requests.post(url, headers=headers, json=test_query)
            
            if response.status_code == 200:
                self.connected = True
                return {
                    'status': 'success',
                    'connected': True,
                    'workspace_id': self.workspace_id
                }
            else:
                self.connected = False
                return {
                    'status': 'error',
                    'connected': False,
                    'error': f'HTTP {response.status_code}: {response.text}'
                }
        except Exception as e:
            self.connected = False
            return {
                'status': 'error',
                'connected': False,
                'error': str(e)
            }
    
    def execute_query(self, query: str, timespan: str = 'P1D') -> Dict[str, Any]:
        """Execute a KQL query on Azure Sentinel"""
        if not self.connected or not self.access_token:
            conn_result = self.test_connection()
            if not conn_result.get('connected'):
                return {
                    'status': 'error',
                    'error': 'Not connected to Azure Sentinel',
                    'results': []
                }
        
        try:
            headers = {
                'Authorization': f'Bearer {self.access_token}',
                'Content-Type': 'application/json'
            }
            
            url = f"https://api.loganalytics.io/v1/workspaces/{self.workspace_id}/query"
            
            query_body = {
                'query': query,
                'timespan': timespan
            }
            
            response = requests.post(url, headers=headers, json=query_body)
            
            if response.status_code == 200:
                data = response.json()
                tables = data.get('tables', [])
                
                results = []
                if tables:
                    columns = tables[0].get('columns', [])
                    rows = tables[0].get('rows', [])
                    
                    for row in rows:
                        result = {}
                        for i, col in enumerate(columns):
                            result[col.get('name')] = row[i] if i < len(row) else None
                        results.append(result)
                
                return {
                    'status': 'success',
                    'result_count': len(results),
                    'results': results[:100]  # Limit to 100 results
                }
            else:
                return {
                    'status': 'error',
                    'error': f'HTTP {response.status_code}: {response.text}',
                    'results': []
                }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e),
                'results': []
            }


class SIEMIntegrationManager:
    """Manager for SIEM integrations"""
    
    def __init__(self):
        self.connectors = {}
    
    def add_connector(self, name: str, connector_type: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """Add a new SIEM connector"""
        try:
            if connector_type.lower() == 'splunk':
                connector = SplunkConnector(config)
            elif connector_type.lower() == 'elasticsearch':
                connector = ElasticsearchConnector(config)
            elif connector_type.lower() == 'sentinel' or connector_type.lower() == 'azure_sentinel':
                connector = AzureSentinelConnector(config)
            else:
                return {
                    'status': 'error',
                    'error': f'Unknown connector type: {connector_type}'
                }
            
            self.connectors[name] = connector
            
            return {
                'status': 'success',
                'message': f'Connector "{name}" added successfully'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def test_connector(self, name: str) -> Dict[str, Any]:
        """Test a specific SIEM connector"""
        if name not in self.connectors:
            return {
                'status': 'error',
                'error': f'Connector "{name}" not found'
            }
        
        return self.connectors[name].test_connection()
    
    def execute_query(self, name: str, query: str, **kwargs) -> Dict[str, Any]:
        """Execute a query on a specific SIEM"""
        if name not in self.connectors:
            return {
                'status': 'error',
                'error': f'Connector "{name}" not found',
                'results': []
            }
        
        return self.connectors[name].execute_query(query, **kwargs)
    
    def get_connectors(self) -> List[str]:
        """Get list of available connectors"""
        return list(self.connectors.keys())
