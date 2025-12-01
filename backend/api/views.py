from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import traceback
import time
from datetime import datetime

from .query_generator import QueryGenerator
from .mitre_attack import MitreAttackIntegration
from .validators import QueryValidator

# Try to import new components (they may not be available initially)
try:
    from .performance_metrics import MetricsCollector, AnalystFeedback
    from .siem_integration import SIEMIntegrationManager
    from .mitre_framework_full import MITREAttackFramework
    from .models import QueryLibrary
    
    metrics_collector = MetricsCollector()
    analyst_feedback = AnalystFeedback()
    siem_manager = SIEMIntegrationManager()
    mitre_framework = MITREAttackFramework()
    NEW_FEATURES_AVAILABLE = True
except ImportError as e:
    print(f"Some new features not available: {e}")
    NEW_FEATURES_AVAILABLE = False

# Initialize core components
query_generator = QueryGenerator()
mitre_attack = MitreAttackIntegration()
query_validator = QueryValidator()

@method_decorator(csrf_exempt, name='dispatch')
class GenerateQueryView(View):
    """Generate threat hunting query from natural language description"""
    
    def post(self, request):
        start_time = time.time()
        success = False
        error_message = None
        
        try:
            # Parse JSON data
            data = json.loads(request.body.decode('utf-8'))
            description = data.get('description', '')
            query_type = data.get('query_type', 'spl')
            include_mitre = data.get('include_mitre', False)
            
            if not description:
                return JsonResponse({
                    'error': 'Description is required'
                }, status=400)
            
            # Generate query using LLM
            query_result = query_generator.generate(description, query_type)
            
            # Get MITRE ATT&CK mapping if requested
            mitre_technique = None
            if include_mitre:
                if NEW_FEATURES_AVAILABLE:
                    # Use full framework
                    techniques = mitre_framework.map_description_to_techniques(description)
                    mitre_technique = techniques[0] if techniques else None
                else:
                    # Use legacy method
                    mitre_technique = mitre_attack.map_to_technique(description)
            
            # Validate query
            validation_result = query_validator.validate(query_result["query"], query_type)
            
            success = True
            generation_time = time.time() - start_time
            
            # Record metrics and save to library if available
            if NEW_FEATURES_AVAILABLE:
                try:
                    # 1. Record metrics
                    metrics_collector.record_query_generation(
                        description=description,
                        query_type=query_type,
                        query=query_result["query"],
                        generation_time=generation_time,
                        validation_result=validation_result,
                        mitre_technique=mitre_technique,
                        success=True
                    )
                    
                    # 2. Save to Query Library
                    mitre_id = mitre_technique.get('id') if mitre_technique else None
                    mitre_name = mitre_technique.get('name') if mitre_technique else None
                    
                    QueryLibrary.objects.create(
                        title=description[:100] + "..." if len(description) > 100 else description,
                        description=description,
                        query_type=query_type,
                        query=query_result["query"],
                        mitre_technique_id=mitre_id,
                        mitre_technique_name=mitre_name,
                        is_valid=validation_result.get('is_valid', True),
                        validation_errors=validation_result.get('errors', []),
                        validation_warnings=validation_result.get('warnings', []),
                        created_by='system'
                    )
                except Exception as e:
                    print(f"Error saving to library/metrics: {e}")
            
            return JsonResponse({
                'query': query_result["query"],
                'explanation': query_result["explanation"],
                'mitre_technique': mitre_technique,
                'validation_result': validation_result,
                'generation_time': generation_time
            })
            
        except json.JSONDecodeError:
            error_message = 'Invalid JSON data'
            return JsonResponse({
                'error': error_message
            }, status=400)
        except Exception as e:
            error_message = str(e)
            generation_time = time.time() - start_time
            
            # Record failed attempt
            if NEW_FEATURES_AVAILABLE:
                try:
                    metrics_collector.record_query_generation(
                        description=data.get('description', '') if 'data' in locals() else '',
                        query_type=data.get('query_type', 'spl') if 'data' in locals() else 'spl',
                        query='',
                        generation_time=generation_time,
                        validation_result={},
                        success=False,
                        error=error_message
                    )
                except:
                    pass
            
            return JsonResponse({
                'error': f'Error generating query: {error_message}',
                'traceback': traceback.format_exc()
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class MitreTechniquesView(View):
    """Get all MITRE ATT&CK techniques"""
    
    def get(self, request):
        try:
            if NEW_FEATURES_AVAILABLE:
                # Use full framework
                techniques = mitre_framework.get_all_techniques()
            else:
                # Use legacy method
                techniques = mitre_attack.get_all_techniques()
            
            return JsonResponse({
                'techniques': techniques,
                'count': len(techniques)
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error fetching MITRE techniques: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class PerformanceMetricsView(View):
    """Get performance metrics and analytics"""
    
    def get(self, request):
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'Performance metrics not available'
            }, status=503)
        
        try:
            summary = metrics_collector.get_summary()
            analytics = metrics_collector.get_performance_analytics()
            time_series = metrics_collector.get_time_series_data(interval='day')
            
            return JsonResponse({
                'summary': summary,
                'analytics': analytics,
                'time_series': time_series
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error fetching metrics: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class QueryLibraryView(View):
    """Manage query library"""
    
    def get(self, request):
        """Get all saved queries"""
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'Query library not available'
            }, status=503)
        
        try:
            queries = QueryLibrary.objects.all().values()
            return JsonResponse({
                'queries': list(queries),
                'count': len(queries)
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error fetching queries: {str(e)}'
            }, status=500)
    
    def post(self, request):
        """Save a new query"""
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'Query library not available'
            }, status=503)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            query = QueryLibrary.objects.create(
                title=data.get('title', ''),
                description=data.get('description', ''),
                query_type=data.get('query_type', 'spl'),
                query=data.get('query', ''),
                mitre_technique_id=data.get('mitre_technique_id'),
                mitre_technique_name=data.get('mitre_technique_name'),
                is_valid=data.get('is_valid', True),
                validation_errors=data.get('validation_errors', []),
                validation_warnings=data.get('validation_warnings', []),
                optimization_suggestions=data.get('optimization_suggestions', []),
                created_by=data.get('created_by', 'system'),
                tags=data.get('tags', [])
            )
            
            return JsonResponse({
                'message': 'Query saved successfully',
                'query_id': query.id
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error saving query: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class SIEMConnectionView(View):
    """Manage SIEM connections"""
    
    def get(self, request):
        """Get all SIEM connections"""
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'SIEM integration not available'
            }, status=503)
        
        try:
            connectors = siem_manager.get_connectors()
            return JsonResponse({
                'connectors': connectors
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error fetching connectors: {str(e)}'
            }, status=500)
    
    def post(self, request):
        """Add a new SIEM connection"""
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'SIEM integration not available'
            }, status=503)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            result = siem_manager.add_connector(
                name=data.get('name'),
                connector_type=data.get('type'),
                config=data.get('config', {})
            )
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({
                'error': f'Error adding connector: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class TestSIEMConnectionView(View):
    """Test a SIEM connection"""
    
    def post(self, request):
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'SIEM integration not available'
            }, status=503)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            connector_name = data.get('name')
            
            result = siem_manager.test_connector(connector_name)
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({
                'error': f'Error testing connection: {str(e)}'
            }, status=500)


@method_decorator(csrf_exempt, name='dispatch')
class ExecuteQueryView(View):
    """Execute a query on a SIEM platform"""
    
    def post(self, request):
        if not NEW_FEATURES_AVAILABLE:
            return JsonResponse({
                'error': 'SIEM integration not available'
            }, status=503)
        
        try:
            data = json.loads(request.body.decode('utf-8'))
            
            result = siem_manager.execute_query(
                name=data.get('siem_name'),
                query=data.get('query'),
                **data.get('params', {})
            )
            
            return JsonResponse(result)
        except Exception as e:
            return JsonResponse({
                'error': f'Error executing query: {str(e)}'
            }, status=500)


class HealthCheckView(View):
    """Health check endpoint"""
    
    def get(self, request):
        return JsonResponse({
            'status': 'healthy',
            'new_features_available': NEW_FEATURES_AVAILABLE,
            'timestamp': datetime.now().isoformat()
        })