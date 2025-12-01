from django.db import models
from django.contrib.auth.models import User
import json


class QueryLibrary(models.Model):
    """Store generated threat hunting queries"""
    
    QUERY_TYPES = [
        ('spl', 'Splunk SPL'),
        ('kql', 'Kusto Query Language'),
        ('dsl', 'Elasticsearch DSL'),
    ]
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Query details
    title = models.CharField(max_length=255, blank=True, default='')
    description = models.TextField(help_text='Natural language threat description')
    query_type = models.CharField(max_length=10, choices=QUERY_TYPES)
    query = models.TextField(help_text='Generated query')
    
    # Metadata
    mitre_technique_id = models.CharField(max_length=20, blank=True, null=True)
    mitre_technique_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Validation
    is_valid = models.BooleanField(default=True)
    validation_errors = models.JSONField(default=list, blank=True)
    validation_warnings = models.JSONField(default=list, blank=True)
    optimization_suggestions = models.JSONField(default=list, blank=True)
    
    # Usage tracking
    execution_count = models.IntegerField(default=0)
    last_executed = models.DateTimeField(null=True, blank=True)
    
    # User management
    created_by = models.CharField(max_length=100, default='system')
    is_template = models.BooleanField(default=False)
    is_public = models.BooleanField(default=False)
    
    # Tags for organization
    tags = models.JSONField(default=list, blank=True)
    
    def __str__(self):
        return f"{self.title or self.description[:50]} ({self.query_type})"
    
    class Meta:
        db_table = 'query_library'
        ordering = ['-created_at']
        verbose_name = 'Query'
        verbose_name_plural = 'Query Library'


class QueryTemplate(models.Model):
    """Pre-defined query templates for common threat hunting scenarios"""
    
    QUERY_TYPES = [
        ('spl', 'Splunk SPL'),
        ('kql', 'Kusto Query Language'),
        ('dsl', 'Elasticsearch DSL'),
    ]
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=255)
    description = models.TextField()
    query_type = models.CharField(max_length=10, choices=QUERY_TYPES)
    template = models.TextField(help_text='Query template with placeholders')
    
    # Categorization
    category = models.CharField(max_length=100, db_index=True)
    mitre_technique_id = models.CharField(max_length=20, blank=True, null=True)
    
    # Parameters for template
    parameters = models.JSONField(
        default=dict,
        help_text='Template parameters with default values'
    )
    
    is_active = models.BooleanField(default=True)
    usage_count = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.name} ({self.query_type})"
    
    class Meta:
        db_table = 'query_template'
        ordering = ['category', 'name']
        verbose_name = 'Query Template'
        verbose_name_plural = 'Query Templates'


class QueryFeedback(models.Model):
    """Store analyst feedback on generated queries"""
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    query = models.ForeignKey(
        QueryLibrary,
        on_delete=models.CASCADE,
        related_name='feedback'
    )
    
    # Ratings (1-5 scale)
    overall_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='Overall satisfaction rating'
    )
    usefulness_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='How useful was the query?'
    )
    accuracy_rating = models.IntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        help_text='How accurate was the query?'
    )
    
    # Comments
    comments = models.TextField(blank=True)
    
    # User
    analyst_name = models.CharField(max_length=100, default='anonymous')
    
    def __str__(self):
        return f"Feedback for {self.query} - Rating: {self.overall_rating}/5"
    
    class Meta:
        db_table = 'query_feedback'
        ordering = ['-created_at']
        verbose_name = 'Query Feedback'
        verbose_name_plural = 'Query Feedback'


class SIEMConnection(models.Model):
    """Store SIEM connection configurations"""
    
    SIEM_TYPES = [
        ('splunk', 'Splunk'),
        ('elasticsearch', 'Elasticsearch'),
        ('sentinel', 'Azure Sentinel'),
    ]
    
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    name = models.CharField(max_length=100, unique=True)
    siem_type = models.CharField(max_length=20, choices=SIEM_TYPES)
    
    # Connection details (stored as JSON for flexibility)
    configuration = models.JSONField(
        help_text='SIEM connection configuration (encrypted in production)'
    )
    
    is_active = models.BooleanField(default=True)
    last_connected = models.DateTimeField(null=True, blank=True)
    connection_status = models.CharField(max_length=50, default='unknown')
    
    def __str__(self):
        return f"{self.name} ({self.siem_type})"
    
    class Meta:
        db_table = 'siem_connection'
        ordering = ['name']
        verbose_name = 'SIEM Connection'
        verbose_name_plural = 'SIEM Connections'


class QueryExecutionLog(models.Model):
    """Log query executions for performance tracking"""
    
    id = models.AutoField(primary_key=True)
    executed_at = models.DateTimeField(auto_now_add=True)
    
    query = models.ForeignKey(
        QueryLibrary,
        on_delete=models.CASCADE,
        related_name='executions',
        null=True,
        blank=True
    )
    
    siem_connection = models.ForeignKey(
        SIEMConnection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Execution details
    execution_time_ms = models.FloatField(help_text='Query execution time in milliseconds')
    result_count = models.IntegerField(default=0)
    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)
    
    # Performance metrics
    memory_usage_mb = models.FloatField(null=True, blank=True)
    cpu_usage_percent = models.FloatField(null=True, blank=True)
    
    def __str__(self):
        status = 'Success' if self.success else 'Failed'
        return f"Execution at {self.executed_at} - {status}"
    
    class Meta:
        db_table = 'query_execution_log'
        ordering = ['-executed_at']
        verbose_name = 'Query Execution Log'
        verbose_name_plural = 'Query Execution Logs'
from django.db import models

# Create your models here.