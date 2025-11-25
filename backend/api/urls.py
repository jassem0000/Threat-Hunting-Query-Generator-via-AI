from django.urls import path
from .views import GenerateQueryView, MitreTechniquesView, HealthCheckView

urlpatterns = [
    path('generate-query', GenerateQueryView.as_view(), name='generate_query'),
    path('mitre-techniques', MitreTechniquesView.as_view(), name='mitre_techniques'),
    path('health', HealthCheckView.as_view(), name='health_check'),
]