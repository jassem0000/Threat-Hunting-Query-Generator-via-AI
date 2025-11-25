from typing import Dict, Any
import json
import requests
import ollama

class QueryGenerator:
    """Generates threat hunting queries from natural language using local LLMs"""
    
    def __init__(self):
        """Initialize the query generator"""
        # Define prompt templates for different query types
        self.prompt_templates = {
            "spl": self._get_spl_prompt(),
            "kql": self._get_kql_prompt(),
            "dsl": self._get_dsl_prompt()
        }
        
    def _get_spl_prompt(self) -> str:
        """Get prompt template for SPL queries"""
        return """
        You are a cybersecurity expert specializing in Splunk SPL (Search Processing Language).
        Convert the following natural language description into a valid SPL query.
        Return ONLY a JSON object with 'query' and 'explanation' fields.
        The explanation should describe what the query does and what it's looking for.
        
        Example output format:
        {{
            "query": "index=security sourcetype=windows EventCode=4625 | stats count by user, src_ip",
            "explanation": "This query searches for Windows authentication failure events (EventCode 4625) and counts them by user and source IP to identify potential brute force attacks."
        }}
        
        Description: {description}
        """
    
    def _get_kql_prompt(self) -> str:
        """Get prompt template for KQL queries"""
        return """
        You are a cybersecurity expert specializing in Kusto Query Language (KQL) for Microsoft Sentinel.
        Convert the following natural language description into a valid KQL query.
        Return ONLY a JSON object with 'query' and 'explanation' fields.
        The explanation should describe what the query does and what it's looking for.
        
        Example output format:
        {{
            "query": "SecurityEvent | where EventID == 4625 | summarize count() by TargetUserName, IpAddress",
            "explanation": "This query searches for Windows authentication failure events (EventID 4625) and counts them by target user name and IP address to identify potential brute force attacks."
        }}
        
        Description: {description}
        """
    
    def _get_dsl_prompt(self) -> str:
        """Get prompt template for Elasticsearch DSL queries"""
        return """
        You are a cybersecurity expert specializing in Elasticsearch DSL queries.
        Convert the following natural language description into a valid Elasticsearch DSL query.
        Return ONLY a JSON object with 'query' and 'explanation' fields.
        The explanation should describe what the query does and what it's looking for.
        
        Example output format:
        {{
            "query": "{{\\"query\\": {{\\"bool\\": {{\\"must\\": [{{\\"match\\": {{\\"event.code\\": \\"4625\\"}}}}], \\"filter\\": [{{\\"range\\": {{\\"@timestamp\\": {{\\"gte\\": \\"now-24h\\"}}}}}}]}}}}}}",
            "explanation": "This query searches for Windows authentication failure events (event.code 4625) in the last 24 hours to identify potential brute force attacks."
        }}
        
        Description: {description}
        """
    
    def generate(self, description: str, query_type: str) -> Dict[str, Any]:
        """
        Generate a threat hunting query from natural language description
        
        Args:
            description: Natural language description of what to hunt for
            query_type: Type of query to generate (spl, kql, dsl)
            
        Returns:
            Dictionary containing the generated query and explanation
        """
        if query_type not in self.prompt_templates:
            raise ValueError(f"Unsupported query type: {query_type}")
        
        # Prepare the prompt
        prompt = self.prompt_templates[query_type].format(description=description)
        
        try:
            # Try to use Ollama first with llama3.2
            response = ollama.chat(model='llama3.2', messages=[
                {
                    'role': 'user',
                    'content': prompt,
                },
            ])
            
            # Parse the response
            content = response['message']['content']
            # Extract JSON from the response
            start = content.find('{')
            end = content.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = content[start:end]
                result = json.loads(json_str)
                return result
            else:
                raise ValueError("Could not extract JSON from LLM response")
                
        except Exception as e:
            # Fallback to direct Ollama API call with llama3.2
            try:
                url = "http://localhost:11434/api/generate"
                payload = {
                    "model": "llama3.2",
                    "prompt": prompt,
                    "stream": False
                }
                
                response = requests.post(url, json=payload)
                response.raise_for_status()
                
                data = response.json()
                content = data.get('response', '')
                
                # Extract JSON from the response
                start = content.find('{')
                end = content.rfind('}') + 1
                if start != -1 and end != 0:
                    json_str = content[start:end]
                    result = json.loads(json_str)
                    return result
                else:
                    raise ValueError("Could not extract JSON from LLM response")
                    
            except Exception as e2:
                # Return a default response if both methods fail
                return {
                    "query": "# Failed to generate query. Please check Ollama installation and model availability.",
                    "explanation": f"Error occurred during query generation: {str(e2)}"
                }