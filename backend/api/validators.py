from typing import Dict, Any, List, Set, Tuple
import re
import json

class QueryValidator:
    """Advanced validator for threat hunting queries with comprehensive syntax checking"""
    
    def __init__(self):
        """Initialize the query validator with language definitions"""
        self._init_spl_definitions()
        self._init_kql_definitions()
        self._init_dsl_definitions()
    
    def _init_spl_definitions(self):
        """Initialize SPL command and function definitions"""
        self.spl_commands = {
            'search', 'where', 'eval', 'stats', 'table', 'fields', 'rename', 'sort',
            'dedup', 'head', 'tail', 'rex', 'regex', 'transaction', 'streamstats',
            'eventstats', 'join', 'append', 'lookup', 'inputlookup', 'outputlookup',
            'bucket', 'chart', 'timechart', 'top', 'rare', 'contingency', 'associate',
            'bin', 'convert', 'fieldformat', 'foreach', 'makemv', 'mvexpand', 'nomv',
            'return', 'sendemail', 'collect', 'sistats', 'tstat', 'tstats', 'mstats',
            'metadata', 'addtotals', 'makecontinuous', 'fillnull', 'filldown'
        }
        
        self.spl_functions = {
            'avg', 'count', 'dc', 'distinct_count', 'earliest', 'earliest_time',
            'latest', 'latest_time', 'max', 'median', 'min', 'mode', 'perc', 
            'percentile', 'range', 'stdev', 'stdevp', 'sum', 'sumsq', 'var', 'varp',
            'values', 'list', 'first', 'last', 'rate', 'abs', 'ceil', 'floor',
            'round', 'exp', 'ln', 'log', 'pow', 'sqrt', 'if', 'case', 'coalesce',
            'isnull', 'isnotnull', 'len', 'lower', 'upper', 'substr', 'replace',
            'trim', 'ltrim', 'rtrim', 'split', 'mvcount', 'mvindex', 'mvjoin',
            'now', 'time', 'strftime', 'strptime', 'relative_time', 'tostring',
            'tonumber', 'match', 'like', 'cidrmatch', 'searchmatch'
        }
        
        self.spl_operators = {'AND', 'OR', 'NOT', '=', '!=', '<', '>', '<=', '>=', 'IN'}
    
    def _init_kql_definitions(self):
        """Initialize KQL operators and function definitions"""
        self.kql_operators = {
            'where', 'project', 'extend', 'summarize', 'distinct', 'top', 'sort',
            'join', 'union', 'let', 'as', 'parse', 'evaluate', 'invoke', 'render',
            'take', 'limit', 'sample', 'count', 'getschema', 'datatable', 'print',
            'search', 'find', 'mv-expand', 'mv-apply', 'make-series', 'order',
            'partition', 'scan', 'serialize', 'facet'
        }
        
        self.kql_functions = {
            'ago', 'now', 'startofday', 'startofweek', 'startofmonth', 'startofyear',
            'endofday', 'endofweek', 'endofmonth', 'endofyear', 'datetime', 'totimespan',
            'bin', 'floor', 'ceiling', 'round', 'abs', 'exp', 'log', 'log10', 'log2',
            'pow', 'sqrt', 'strlen', 'substring', 'tolower', 'toupper', 'strcat',
            'split', 'replace', 'trim', 'countof', 'extract', 'extract_all', 'parse_json',
            'parse_xml', 'parse_csv', 'bag_keys', 'bag_merge', 'pack', 'pack_all',
            'todynamic', 'tostring', 'toint', 'tolong', 'todouble', 'tobool', 'todatetime',
            'isnull', 'isnotnull', 'isempty', 'isnotempty', 'count', 'dcount', 'dcountif',
            'sum', 'sumif', 'avg', 'avgif', 'min', 'minif', 'max', 'maxif', 'any',
            'make_list', 'make_set', 'percentile', 'stdev', 'variance', 'arg_max',
            'arg_min', 'take_any', 'take_anyif', 'hll', 'hll_merge', 'tdigest',
            'contains', 'contains_cs', 'has', 'has_cs', 'hasprefix', 'hassuffix',
            'in', 'in~', '!in', '!in~', 'matches regex', 'between', 'and', 'or', 'not'
        }
        
        self.kql_comparison_ops = {'==', '!=', '<', '>', '<=', '>=', '=~', '!~', 'contains', 'startswith', 'endswith', 'matches', 'has'}
    
    def _init_dsl_definitions(self):
        """Initialize Elasticsearch DSL definitions"""
        self.dsl_query_types = {
            'match', 'match_all', 'match_phrase', 'match_phrase_prefix', 'multi_match',
            'term', 'terms', 'terms_set', 'range', 'exists', 'prefix', 'wildcard',
            'regexp', 'fuzzy', 'type', 'ids', 'bool', 'boosting', 'constant_score',
            'dis_max', 'function_score', 'nested', 'has_child', 'has_parent',
            'parent_id', 'geo_bounding_box', 'geo_distance', 'geo_polygon',
            'geo_shape', 'more_like_this', 'percolate', 'rank_feature', 'script',
            'script_score', 'wrapper', 'pinned', 'span_term', 'span_multi',
            'span_first', 'span_near', 'span_or', 'span_not', 'span_containing',
            'span_within', 'field_masking_span', 'distance_feature', 'query_string',
            'simple_query_string'
        }
        
        self.dsl_aggregation_types = {
            'avg', 'weighted_avg', 'cardinality', 'extended_stats', 'geo_bounds',
            'geo_centroid', 'geo_line', 'max', 'median_absolute_deviation', 'min',
            'percentiles', 'percentile_ranks', 'scripted_metric', 'stats', 'string_stats',
            'sum', 'top_hits', 'top_metrics', 'value_count', 'boxplot', 't_test',
            'rate', 'adjacency_matrix', 'auto_date_histogram', 'children', 'composite',
            'date_histogram', 'date_range', 'diversified_sampler', 'filter', 'filters',
            'geo_distance', 'geo_hash_grid', 'geo_tile_grid', 'global', 'histogram',
            'ip_range', 'missing', 'multi_terms', 'nested', 'parent', 'random_sampler',
            'range', 'rare_terms', 'reverse_nested', 'sampler', 'significant_terms',
            'significant_text', 'terms', 'variable_width_histogram'
        }
    
    def validate(self, query: str, query_type: str) -> Dict[str, Any]:
        """
        Validate a threat hunting query with comprehensive syntax checking
        
        Args:
            query: The query to validate
            query_type: Type of query (spl, kql, dsl)
            
        Returns:
            Dictionary with validation results including errors, warnings, and suggestions
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
                "optimization_suggestions": [],
                "syntax_score": 0
            }
    
    def _validate_spl(self, query: str) -> Dict[str, Any]:
        """Comprehensive SPL query validation with syntax parsing"""
        errors = []
        warnings = []
        suggestions = []
        
        if not query.strip():
            return self._error_response("Query is empty")
        
        # Normalize query
        normalized = query.strip()
        
        # Check for balanced parentheses and brackets
        balance_errors = self._check_balanced_delimiters(normalized)
        errors.extend(balance_errors)
        
        # Check for balanced quotes
        quote_errors = self._check_balanced_quotes(normalized)
        errors.extend(quote_errors)
        
        # Split by pipes to get commands
        commands = [cmd.strip() for cmd in normalized.split('|') if cmd.strip()]
        
        if not commands:
            errors.append("No valid commands found in query")
            return self._build_response(errors, warnings, suggestions)
        
        # Validate first command (search or index specification)
        first_cmd = commands[0].lower()
        if not (first_cmd.startswith('search') or 'index=' in first_cmd or 'source=' in first_cmd or 'sourcetype=' in first_cmd):
            if not any(cmd in first_cmd for cmd in ['inputlookup', 'metadata', 'tstats', 'datamodel']):
                warnings.append("Query should typically start with 'search' or index/source specification")
        
        # Validate each piped command
        for i, cmd in enumerate(commands):
            cmd_errors, cmd_warnings, cmd_suggestions = self._validate_spl_command(cmd, i)
            errors.extend(cmd_errors)
            warnings.extend(cmd_warnings)
            suggestions.extend(cmd_suggestions)
        
        # Check for field extractions without proper syntax
        if 'rex' in normalized.lower():
            rex_errors = self._validate_rex_syntax(normalized)
            errors.extend(rex_errors)
        
        # Performance checks
        perf_suggestions = self._check_spl_performance(normalized, commands)
        suggestions.extend(perf_suggestions)
        
        # Security checks
        security_warnings = self._check_spl_security(normalized)
        warnings.extend(security_warnings)
        
        syntax_score = self._calculate_syntax_score(errors, warnings)
        
        return self._build_response(errors, warnings, suggestions, syntax_score)
    
    def _validate_spl_command(self, cmd: str, position: int) -> Tuple[List[str], List[str], List[str]]:
        """Validate individual SPL command"""
        errors = []
        warnings = []
        suggestions = []
        
        cmd_lower = cmd.lower().strip()
        
        # Extract command name
        cmd_name = cmd_lower.split()[0] if cmd_lower.split() else ""
        
        # Check if command exists
        if position > 0 and cmd_name and cmd_name not in self.spl_commands:
            # Check if it's a search term (first command can be search terms)
            if not any(op in cmd for op in ['=', '>', '<', '!=', 'AND', 'OR', 'NOT']):
                errors.append(f"Unknown SPL command: '{cmd_name}'")
        
        # Validate stats command
        if cmd_name == 'stats':
            if not any(func in cmd_lower for func in ['count', 'avg', 'sum', 'min', 'max', 'dc', 'values', 'list']):
                warnings.append("stats command should include aggregation functions (count, avg, sum, etc.)")
            if ' by ' in cmd_lower:
                by_clause = cmd_lower.split(' by ')[1]
                if not by_clause.strip():
                    errors.append("stats 'by' clause is empty")
        
        # Validate eval command
        if cmd_name == 'eval':
            if '=' not in cmd:
                errors.append("eval command requires field assignment (field=expression)")
            else:
                # Check for invalid function usage
                eval_expr = cmd.split('=', 1)[1] if '=' in cmd else ""
                func_errors = self._validate_spl_functions(eval_expr)
                errors.extend(func_errors)
        
        # Validate where command
        if cmd_name == 'where':
            if len(cmd.split()) < 2:
                errors.append("where command requires a condition")
            else:
                condition = ' '.join(cmd.split()[1:])
                if not any(op in condition for op in ['=', '>', '<', '!=', 'like', 'match']):
                    warnings.append("where condition should include comparison operators")
        
        # Validate fields command
        if cmd_name == 'fields':
            if '+' in cmd and '-' in cmd:
                warnings.append("Mixing field inclusion (+) and exclusion (-) can be confusing")
            if len(cmd.split()) < 2:
                errors.append("fields command requires field names")
        
        # Validate table command
        if cmd_name == 'table':
            if len(cmd.split()) < 2:
                warnings.append("table command should specify fields to display")
        
        # Validate join command
        if cmd_name == 'join':
            if ' [' not in cmd or ']' not in cmd:
                errors.append("join command requires subsearch in square brackets")
            if not any(join_type in cmd_lower for join_type in ['type=', 'left', 'inner', 'outer']):
                suggestions.append("Consider specifying join type (type=left, type=inner, etc.)")
        
        # Validate rex command
        if cmd_name == 'rex':
            if 'field=' not in cmd_lower and position > 0:
                warnings.append("rex should specify source field with field= parameter")
            if '"(?<' not in cmd and "'(?<" not in cmd:
                warnings.append("rex should use named capture groups (?<fieldname>pattern)")
        
        return errors, warnings, suggestions
    
    def _validate_spl_functions(self, expression: str) -> List[str]:
        """Validate SPL function usage in expressions"""
        errors = []
        
        # Find all function calls
        func_pattern = r'(\w+)\s*\('
        functions = re.findall(func_pattern, expression.lower())
        
        for func in functions:
            if func not in self.spl_functions and func not in ['if', 'case', 'coalesce']:
                errors.append(f"Unknown or invalid SPL function: '{func}'")
        
        # Check for unbalanced parentheses in functions
        paren_count = expression.count('(') - expression.count(')')
        if paren_count != 0:
            errors.append(f"Unbalanced parentheses in expression: {paren_count} unclosed")
        
        return errors
    
    def _validate_rex_syntax(self, query: str) -> List[str]:
        """Validate rex command regex syntax"""
        errors = []
        
        # Find rex commands
        rex_commands = re.findall(r'\|\s*rex[^|]*', query, re.IGNORECASE)
        
        for rex_cmd in rex_commands:
            # Check for named groups
            if '(?<' not in rex_cmd and '(?P<' not in rex_cmd:
                errors.append("rex command should use named capture groups")
            
            # Check for properly quoted regex
            if not ('"' in rex_cmd or "'" in rex_cmd):
                errors.append("rex regex pattern should be quoted")
        
        return errors
    
    def _check_spl_performance(self, query: str, commands: List[str]) -> List[str]:
        """Check for SPL performance issues"""
        suggestions = []
        
        # Check for time bounds
        if not any(bound in query for bound in ['earliest=', 'latest=', 'earliest:', 'latest:']):
            suggestions.append("Add time bounds (earliest=/latest=) to improve search performance")
        
        # Check for index specification
        if 'index=' not in query.lower() and not query.lower().startswith('| '):
            suggestions.append("Specify index to narrow search scope")
        
        # Check for wildcards at start of search terms
        if re.search(r'\s\*\w+', query):
            warnings = ["Leading wildcards (*term) cause slow searches"]
            return warnings + suggestions
        
        # Check for stats before other commands
        stats_position = next((i for i, cmd in enumerate(commands) if cmd.lower().startswith('stats')), -1)
        if stats_position > -1:
            if any(cmd.lower().startswith(('table', 'fields')) for cmd in commands[stats_position + 1:]):
                suggestions.append("Consider using 'table' or 'fields' before 'stats' for better performance")
        
        # Check for unnecessary regex
        if query.count('rex') > 2:
            suggestions.append("Multiple rex commands may impact performance; consider combining patterns")
        
        # Check for dedup usage
        if 'dedup' in query.lower() and stats_position > -1:
            if stats_position < commands.index(next(cmd for cmd in commands if 'dedup' in cmd.lower())):
                suggestions.append("Apply dedup before stats for better performance")
        
        return suggestions
    
    def _check_spl_security(self, query: str) -> List[str]:
        """Check for potential security issues in SPL"""
        warnings = []
        
        # Check for overly broad searches
        if query.strip() == 'search *' or query.strip().startswith('* |'):
            warnings.append("Overly broad search (search *) may expose sensitive data")
        
        # Check for password/credential fields
        sensitive_fields = ['password', 'passwd', 'pwd', 'secret', 'token', 'api_key', 'apikey']
        query_lower = query.lower()
        for field in sensitive_fields:
            if field in query_lower and 'table' in query_lower:
                warnings.append(f"Query may expose sensitive field: {field}")
        
        return warnings
    
    def _validate_kql(self, query: str) -> Dict[str, Any]:
        """Comprehensive KQL query validation with syntax parsing"""
        errors = []
        warnings = []
        suggestions = []
        
        if not query.strip():
            return self._error_response("Query is empty")
        
        normalized = query.strip()
        
        # Check balanced delimiters
        balance_errors = self._check_balanced_delimiters(normalized)
        errors.extend(balance_errors)
        
        # Check balanced quotes
        quote_errors = self._check_balanced_quotes(normalized)
        errors.extend(quote_errors)
        
        # Split by pipes
        operators = [op.strip() for op in normalized.split('|') if op.strip()]
        
        if not operators:
            errors.append("No valid operators found in query")
            return self._build_response(errors, warnings, suggestions)
        
        # Validate table name (first part)
        first_part = operators[0]
        if not self._is_valid_kql_table(first_part):
            warnings.append("Query should start with a table name (e.g., SecurityEvent, Syslog)")
        
        # Validate each operator
        for i, op in enumerate(operators):
            op_errors, op_warnings, op_suggestions = self._validate_kql_operator(op, i)
            errors.extend(op_errors)
            warnings.extend(op_warnings)
            suggestions.extend(op_suggestions)
        
        # Performance checks
        perf_suggestions = self._check_kql_performance(normalized, operators)
        suggestions.extend(perf_suggestions)
        
        # Security checks
        security_warnings = self._check_kql_security(normalized)
        warnings.extend(security_warnings)
        
        syntax_score = self._calculate_syntax_score(errors, warnings)
        
        return self._build_response(errors, warnings, suggestions, syntax_score)
    
    def _is_valid_kql_table(self, first_part: str) -> bool:
        """Check if first part looks like a valid KQL table"""
        # Common KQL table patterns
        if re.match(r'^[A-Z][a-zA-Z0-9_]*$', first_part.split()[0]):
            return True
        # Let statements
        if first_part.lower().startswith('let '):
            return True
        # Print/search statements
        if first_part.lower().startswith(('print', 'search', 'find', 'union')):
            return True
        return False
    
    def _validate_kql_operator(self, op: str, position: int) -> Tuple[List[str], List[str], List[str]]:
        """Validate individual KQL operator"""
        errors = []
        warnings = []
        suggestions = []
        
        op_lower = op.lower().strip()
        
        # Skip table name validation for first operator
        if position == 0:
            return errors, warnings, suggestions
        
        # Extract operator name
        op_name = op_lower.split()[0] if op_lower.split() else ""
        
        # Check if operator exists
        if op_name and op_name not in self.kql_operators:
            if not any(func in op_lower for func in self.kql_functions):
                errors.append(f"Unknown KQL operator: '{op_name}'")
        
        # Validate where operator
        if op_name == 'where':
            if len(op.split()) < 2:
                errors.append("where operator requires a condition")
            else:
                condition = ' '.join(op.split()[1:])
                if not any(comp in condition for comp in ['==', '!=', '>', '<', '>=', '<=', 'contains', 'startswith', 'has']):
                    warnings.append("where condition should include comparison operators")
                
                # Check for common mistakes
                if ' = ' in condition and ' == ' not in condition:
                    errors.append("Use '==' for equality comparison, not '='")
        
        # Validate project operator
        if op_name == 'project':
            if len(op.split()) < 2:
                errors.append("project operator requires field names")
        
        # Validate summarize operator
        if op_name == 'summarize':
            if not any(agg in op_lower for agg in ['count(', 'sum(', 'avg(', 'min(', 'max(', 'dcount(', 'make_set(', 'make_list(']):
                warnings.append("summarize should include aggregation functions")
            if ' by ' in op_lower:
                by_clause = op_lower.split(' by ')[1]
                if not by_clause.strip():
                    errors.append("summarize 'by' clause is empty")
        
        # Validate extend operator
        if op_name == 'extend':
            if '=' not in op:
                errors.append("extend operator requires field assignment (field = expression)")
        
        # Validate join operator
        if op_name == 'join':
            if 'kind=' not in op_lower:
                suggestions.append("Specify join kind (inner, leftouter, rightouter, fullouter)")
            if ' on ' not in op_lower and ' $left' not in op_lower:
                warnings.append("join should specify 'on' condition")
        
        # Validate parse operator
        if op_name == 'parse':
            if 'with' not in op_lower:
                warnings.append("parse operator should specify pattern 'with' clause")
        
        return errors, warnings, suggestions
    
    def _check_kql_performance(self, query: str, operators: List[str]) -> List[str]:
        """Check for KQL performance issues"""
        suggestions = []
        
        # Check for time filtering
        if not any(time_ref in query for time_ref in ['TimeGenerated', 'Timestamp', 'ago(', 'startofday', 'between']):
            suggestions.append("Add time filtering (e.g., | where TimeGenerated > ago(24h)) for better performance")
        
        # Check where position
        where_position = next((i for i, op in enumerate(operators) if op.lower().strip().startswith('where')), -1)
        if where_position > 2:
            suggestions.append("Move 'where' filters earlier in the query for better performance")
        
        # Check for expensive operations
        if 'contains' in query.lower():
            suggestions.append("Consider using 'has' instead of 'contains' for better performance with word matches")
        
        if query.lower().count('join') > 1:
            suggestions.append("Multiple joins may impact performance; consider query optimization")
        
        # Check for select before summarize
        summarize_pos = next((i for i, op in enumerate(operators) if op.lower().startswith('summarize')), -1)
        project_pos = next((i for i, op in enumerate(operators) if op.lower().startswith('project')), -1)
        
        if summarize_pos > -1 and project_pos > summarize_pos:
            suggestions.append("Use 'project' before 'summarize' to reduce data processed")
        
        return suggestions
    
    def _check_kql_security(self, query: str) -> List[str]:
        """Check for potential security issues in KQL"""
        warnings = []
        
        # Check for sensitive data exposure
        sensitive_fields = ['password', 'secret', 'token', 'key', 'credential']
        if any(field in query.lower() for field in sensitive_fields):
            if 'project' in query.lower() or 'extend' in query.lower():
                warnings.append("Query may expose sensitive fields")
        
        return warnings
    
    def _validate_dsl(self, query: str) -> Dict[str, Any]:
        """Comprehensive Elasticsearch DSL query validation"""
        errors = []
        warnings = []
        suggestions = []
        
        if not query.strip():
            return self._error_response("Query is empty")
        
        # Try to parse JSON
        try:
            parsed = json.loads(query)
        except json.JSONDecodeError as e:
            return self._error_response(f"Invalid JSON structure: {str(e)} at position {e.pos}")
        
        # Validate query structure
        struct_errors, struct_warnings = self._validate_dsl_structure(parsed)
        errors.extend(struct_errors)
        warnings.extend(struct_warnings)
        
        # Validate query types
        if 'query' in parsed:
            query_errors = self._validate_dsl_query_types(parsed['query'])
            errors.extend(query_errors)
        
        # Validate aggregations
        if 'aggs' in parsed or 'aggregations' in parsed:
            agg_key = 'aggs' if 'aggs' in parsed else 'aggregations'
            agg_errors = self._validate_dsl_aggregations(parsed[agg_key])
            errors.extend(agg_errors)
        
        # Performance checks
        perf_suggestions = self._check_dsl_performance(parsed)
        suggestions.extend(perf_suggestions)
        
        # Security checks
        security_warnings = self._check_dsl_security(parsed)
        warnings.extend(security_warnings)
        
        syntax_score = self._calculate_syntax_score(errors, warnings)
        
        return self._build_response(errors, warnings, suggestions, syntax_score)
    
    def _validate_dsl_structure(self, parsed: Dict) -> Tuple[List[str], List[str]]:
        """Validate basic DSL structure"""
        errors = []
        warnings = []
        
        valid_top_keys = {'query', 'aggs', 'aggregations', 'size', 'from', 'sort', '_source', 
                          'fields', 'script_fields', 'docvalue_fields', 'post_filter', 
                          'highlight', 'rescore', 'search_after', 'collapse', 'timeout',
                          'terminate_after', 'min_score', 'track_scores', 'track_total_hits',
                          'indices_boost', 'search_type', 'scroll', 'pit', 'runtime_mappings'}
        
        for key in parsed.keys():
            if key not in valid_top_keys:
                warnings.append(f"Unusual top-level key: '{key}'")
        
        if 'query' not in parsed and 'aggs' not in parsed and 'aggregations' not in parsed:
            warnings.append("DSL should contain 'query' or 'aggs' field")
        
        return errors, warnings
    
    def _validate_dsl_query_types(self, query_obj: Any, path: str = "query") -> List[str]:
        """Recursively validate DSL query types"""
        errors = []
        
        if not isinstance(query_obj, dict):
            errors.append(f"Query at '{path}' should be an object")
            return errors
        
        for query_type, query_content in query_obj.items():
            if query_type not in self.dsl_query_types and query_type != 'must' and query_type != 'should' and query_type != 'must_not' and query_type != 'filter':
                errors.append(f"Unknown query type: '{query_type}' at '{path}'")
            
            # Validate bool query
            if query_type == 'bool':
                if not isinstance(query_content, dict):
                    errors.append(f"bool query at '{path}' should contain an object")
                else:
                    valid_bool_keys = {'must', 'should', 'must_not', 'filter', 'minimum_should_match', 'boost'}
                    for key in query_content.keys():
                        if key not in valid_bool_keys:
                            errors.append(f"Invalid bool query key: '{key}' at '{path}.{query_type}'")
                    
                    # Recursively validate nested queries
                    for clause in ['must', 'should', 'must_not', 'filter']:
                        if clause in query_content:
                            if isinstance(query_content[clause], list):
                                for i, sub_query in enumerate(query_content[clause]):
                                    errors.extend(self._validate_dsl_query_types(sub_query, f"{path}.{query_type}.{clause}[{i}]"))
                            elif isinstance(query_content[clause], dict):
                                errors.extend(self._validate_dsl_query_types(query_content[clause], f"{path}.{query_type}.{clause}"))
            
            # Validate range query
            if query_type == 'range':
                if isinstance(query_content, dict):
                    for field, range_params in query_content.items():
                        if isinstance(range_params, dict):
                            valid_range_keys = {'gt', 'gte', 'lt', 'lte', 'boost', 'format', 'time_zone', 'relation'}
                            for key in range_params.keys():
                                if key not in valid_range_keys:
                                    errors.append(f"Invalid range parameter: '{key}' at '{path}.{query_type}.{field}'")
        
        return errors
    
    def _validate_dsl_aggregations(self, aggs_obj: Dict, path: str = "aggs") -> List[str]:
        """Validate DSL aggregations"""
        errors = []
        
        if not isinstance(aggs_obj, dict):
            errors.append(f"Aggregations at '{path}' should be an object")
            return errors
        
        for agg_name, agg_content in aggs_obj.items():
            if not isinstance(agg_content, dict):
                errors.append(f"Aggregation '{agg_name}' should be an object")
                continue
            
            # Find the aggregation type
            agg_types = [key for key in agg_content.keys() if key in self.dsl_aggregation_types]
            
            if not agg_types:
                # Check for sub-aggregations
                if 'aggs' not in agg_content and 'aggregations' not in agg_content:
                    errors.append(f"Unknown aggregation type in '{agg_name}'")
            
            # Recursively validate nested aggregations
            if 'aggs' in agg_content:
                errors.extend(self._validate_dsl_aggregations(agg_content['aggs'], f"{path}.{agg_name}.aggs"))
            if 'aggregations' in agg_content:
                errors.extend(self._validate_dsl_aggregations(agg_content['aggregations'], f"{path}.{agg_name}.aggregations"))
        
        return errors
    
    def _check_dsl_performance(self, parsed: Dict) -> List[str]:
        """Check for DSL performance issues"""
        suggestions = []
        
        # Check for time range filtering
        query_str = json.dumps(parsed)
        if '@timestamp' not in query_str and 'timestamp' not in query_str.lower():
            suggestions.append("Add time range filtering using @timestamp for better performance")
        
        # Check for size parameter
        if 'size' not in parsed:
            suggestions.append("Specify 'size' parameter to limit results")
        elif parsed['size'] > 10000:
            suggestions.append("Large 'size' values (>10000) may impact performance; consider using scroll or search_after")
        
        # Check for wildcard queries
        if 'wildcard' in query_str or 'prefix' in query_str:
            suggestions.append("Wildcard and prefix queries can be slow; consider using n-grams or edge n-grams")
        
        # Check for script usage
        if 'script' in query_str:
            suggestions.append("Scripts can impact performance; ensure they are optimized and cached")
        
        # Check for nested queries
        if 'nested' in query_str:
            suggestions.append("Nested queries can be expensive; ensure they are necessary")
        
        return suggestions
    
    def _check_dsl_security(self, parsed: Dict) -> List[str]:
        """Check for potential security issues in DSL"""
        warnings = []
        
        query_str = json.dumps(parsed)
        
        # Check for scripting
        if 'script' in query_str:
            warnings.append("Inline scripts may pose security risks; use stored scripts when possible")
        
        # Check for sensitive field exposure
        sensitive_patterns = ['password', 'secret', 'token', 'key', 'credential']
        if any(pattern in query_str.lower() for pattern in sensitive_patterns):
            warnings.append("Query may access or expose sensitive fields")
        
        return warnings
    
    def _check_balanced_delimiters(self, query: str) -> List[str]:
        """Check for balanced parentheses, brackets, and braces"""
        errors = []
        
        delimiters = {'(': ')', '[': ']', '{': '}'}
        stack = []
        
        for i, char in enumerate(query):
            if char in delimiters.keys():
                stack.append((char, i))
            elif char in delimiters.values():
                if not stack:
                    errors.append(f"Unmatched closing '{char}' at position {i}")
                else:
                    opening, pos = stack.pop()
                    if delimiters[opening] != char:
                        errors.append(f"Mismatched delimiters: '{opening}' at position {pos} and '{char}' at position {i}")
        
        for opening, pos in stack:
            errors.append(f"Unclosed '{opening}' at position {pos}")
        
        return errors
    
    def _check_balanced_quotes(self, query: str) -> List[str]:
        """Check for balanced quotes"""
        errors = []
        
        # Check double quotes
        double_quote_count = query.count('"')
        if double_quote_count % 2 != 0:
            errors.append(f"Unbalanced double quotes (found {double_quote_count})")
        
        # Check single quotes
        single_quote_count = query.count("'")
        if single_quote_count % 2 != 0:
            errors.append(f"Unbalanced single quotes (found {single_quote_count})")
        
        return errors
    
    def _calculate_syntax_score(self, errors: List[str], warnings: List[str]) -> int:
        """Calculate a syntax quality score (0-100)"""
        if errors:
            return max(0, 50 - len(errors) * 10)
        if warnings:
            return max(70, 100 - len(warnings) * 5)
        return 100
    
    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Build error response"""
        return {
            "valid": False,
            "errors": [error_msg],
            "warnings": [],
            "optimization_suggestions": [],
            "syntax_score": 0
        }
    
    def _build_response(self, errors: List[str], warnings: List[str], 
                       suggestions: List[str], syntax_score: int = None) -> Dict[str, Any]:
        """Build validation response"""
        if syntax_score is None:
            syntax_score = self._calculate_syntax_score(errors, warnings)
        
        return {
            "valid": len(errors) == 0,
            "errors": list(set(errors)),  # Remove duplicates
            "warnings": list(set(warnings)),
            "optimization_suggestions": list(set(suggestions)),
            "syntax_score": syntax_score
        }