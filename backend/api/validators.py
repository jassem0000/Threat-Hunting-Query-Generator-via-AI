from typing import Dict, Any, Tuple
import re
import json

class QueryValidator:
    """Validates and optimizes threat hunting queries"""
    
    def __init__(self):
        """Initialize the query validator"""
        pass
    
    def validate(self, query: str, query_type: str) -> Dict[str, Any]:
        """
        Validate a threat hunting query
        
        Args:
            query: The query to validate
            query_type: Type of query (spl, kql, dsl)
            
        Returns:
            Dictionary with validation results
        """
        if query_type == "spl":
            return self._validate_spl(query)
        elif query_type == "kql":
            return self._validate_kql(query)
        elif query_type == "dsl":
            return self._validate_dsl(query)
        else:
            return {
                "valid": False,
                "errors": [f"Unsupported query type: {query_type}"],
                "warnings": [],
                "optimization_suggestions": []
            }
    
    def _validate_spl(self, query: str) -> Dict[str, Any]:
        """Validate SPL query"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for basic SPL syntax elements
        if not query.strip():
            errors.append("Query is empty")
        
        # Check for common SPL commands
        spl_commands = ['search', 'index', 'sourcetype', 'stats', 'eval', 'where', 'table']
        has_command = any(cmd in query.lower() for cmd in spl_commands)
        if not has_command:
            warnings.append("Query doesn't appear to contain standard SPL commands")
        
        # Check for time bounding
        time_bounds = ['earliest', 'latest', '_raw', '_time']
        has_time = any(time_bound in query for time_bound in time_bounds)
        if not has_time:
            suggestions.append("Consider adding time bounds to limit search scope")
        
        # Check for performance optimizations
        if '|' not in query:
            suggestions.append("Consider using pipe operators to chain commands for better performance")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "optimization_suggestions": suggestions
        }
    
    def _validate_kql(self, query: str) -> Dict[str, Any]:
        """Validate KQL query"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for basic KQL syntax elements
        if not query.strip():
            errors.append("Query is empty")
        
        # Check for table or materialized view reference
        if '|' not in query:
            warnings.append("Query should typically start with a table or materialized view name followed by a pipe")
        
        # Check for time filtering
        time_filters = ['TimeGenerated', 'Timestamp']
        has_time_filter = any(time_filter in query for time_filter in time_filters)
        if not has_time_filter:
            suggestions.append("Add time filtering to limit search scope (e.g., | where TimeGenerated > ago(24h))")
        
        # Check for common KQL patterns
        kql_patterns = [r'\|\s*where\s+', r'\|\s*summarize\s+', r'\|\s*project\s+']
        has_patterns = any(re.search(pattern, query, re.IGNORECASE) for pattern in kql_patterns)
        if not has_patterns:
            suggestions.append("Consider using where, summarize, or project operators for better query structure")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "optimization_suggestions": suggestions
        }
    
    def _validate_dsl(self, query: str) -> Dict[str, Any]:
        """Validate Elasticsearch DSL query"""
        errors = []
        warnings = []
        suggestions = []
        
        # Check for basic DSL structure
        if not query.strip():
            errors.append("Query is empty")
        
        try:
            # Try to parse as JSON
            parsed = json.loads(query)
            
            # Check for required DSL structure
            if 'query' not in parsed:
                warnings.append("DSL query should typically contain a 'query' field")
            
            # Check for time filtering
            if 'range' not in query and '@timestamp' not in query:
                suggestions.append("Consider adding time range filtering using @timestamp field")
                
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON structure: {str(e)}")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "optimization_suggestions": suggestions
        }