from django.urls import path
from .views import (
    GenerateQueryView, MitreTechniquesView, HealthCheckView,
    PerformanceMetricsView, QueryLibraryView, SIEMConnectionView,
    TestSIEMConnectionView, ExecuteQueryView
)

urlpatterns = [
    # Core endpoints
    path('generate-query', GenerateQueryView.as_view(), name='generate_query'),
    path('mitre-techniques', MitreTechniquesView.as_view(), name='mitre_techniques'),
    path('health', HealthCheckView.as_view(), name='health_check'),
    
    # Performance & Analytics
    path('metrics', PerformanceMetricsView.as_view(), name='performance_metrics'),
    
    # Query Library
    path('queries', QueryLibraryView.as_view(), name='query_library'),
    
    # SIEM Integration
    path('siem/connections', SIEMConnectionView.as_view(), name='siem_connections'),
    path('siem/test', TestSIEMConnectionView.as_view(), name='test_siem'),
    path('siem/execute', ExecuteQueryView.as_view(), name='execute_query'),
]