from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
import json
import traceback

from .query_generator import QueryGenerator
from .mitre_attack import MitreAttackIntegration
from .validators import QueryValidator

# Initialize components
query_generator = QueryGenerator()
mitre_attack = MitreAttackIntegration()
query_validator = QueryValidator()

@method_decorator(csrf_exempt, name='dispatch')
class GenerateQueryView(View):
    """Generate threat hunting query from natural language description"""
    
    def post(self, request):
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
                mitre_technique = mitre_attack.map_to_technique(description)
            
            # Validate query
            validation_result = query_validator.validate(query_result["query"], query_type)
            
            return JsonResponse({
                'query': query_result["query"],
                'explanation': query_result["explanation"],
                'mitre_technique': mitre_technique,
                'validation_result': validation_result
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Invalid JSON data'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'error': f'Error generating query: {str(e)}',
                'traceback': traceback.format_exc()
            }, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class MitreTechniquesView(View):
    """Get all MITRE ATT&CK techniques"""
    
    def get(self, request):
        try:
            techniques = mitre_attack.get_all_techniques()
            return JsonResponse({
                'techniques': techniques
            })
        except Exception as e:
            return JsonResponse({
                'error': f'Error fetching MITRE techniques: {str(e)}'
            }, status=500)

class HealthCheckView(View):
    """Health check endpoint"""
    
    def get(self, request):
        return JsonResponse({
            'status': 'healthy'
        })