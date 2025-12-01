"""
Performance Metrics Module
Tracks and analyzes query generation performance, accuracy, and usage
"""

import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from pathlib import Path
import os


class MetricsCollector:
    """Collects and stores performance metrics"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), '..', 'metrics_data')
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.metrics_file = self.storage_dir / 'metrics.json'
        self.metrics = self._load_metrics()
    
    def _load_metrics(self) -> Dict[str, Any]:
        """Load metrics from storage"""
        if self.metrics_file.exists():
            try:
                with open(self.metrics_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading metrics: {e}")
                return self._initialize_metrics()
        else:
            return self._initialize_metrics()
    
    def _initialize_metrics(self) -> Dict[str, Any]:
        """Initialize empty metrics structure"""
        return {
            'queries': [],
            'summary': {
                'total_queries': 0,
                'successful_queries': 0,
                'failed_queries': 0,
                'average_generation_time': 0,
                'average_validation_score': 0,
                'query_types': {
                    'spl': 0,
                    'kql': 0,
                    'dsl': 0
                },
                'mitre_mappings': 0
            },
            'version': '1.0'
        }
    
    def _save_metrics(self):
        """Save metrics to storage"""
        try:
            with open(self.metrics_file, 'w') as f:
                json.dump(self.metrics, f, indent=2)
        except Exception as e:
            print(f"Error saving metrics: {e}")
    
    def record_query_generation(
        self,
        description: str,
        query_type: str,
        query: str,
        generation_time: float,
        validation_result: Dict[str, Any],
        mitre_technique: Optional[Dict[str, Any]] = None,
        execution_result: Optional[Dict[str, Any]] = None,
        success: bool = True,
        error: Optional[str] = None
    ) -> str:
        """Record a query generation event"""
        
        query_id = f"query_{int(time.time() * 1000)}"
        
        query_record = {
            'id': query_id,
            'timestamp': datetime.now().isoformat(),
            'description': description,
            'query_type': query_type,
            'query': query,
            'generation_time_ms': round(generation_time * 1000, 2),
            'success': success,
            'error': error,
            'validation': {
                'valid': validation_result.get('valid', False),
                'errors': validation_result.get('errors', []),
                'warnings': validation_result.get('warnings', []),
                'optimization_suggestions': validation_result.get('optimization_suggestions', [])
            },
            'mitre_technique': mitre_technique,
            'execution_result': execution_result
        }
        
        # Add to queries list
        self.metrics['queries'].append(query_record)
        
        # Update summary
        self.metrics['summary']['total_queries'] += 1
        
        if success:
            self.metrics['summary']['successful_queries'] += 1
        else:
            self.metrics['summary']['failed_queries'] += 1
        
        self.metrics['summary']['query_types'][query_type] = \
            self.metrics['summary']['query_types'].get(query_type, 0) + 1
        
        if mitre_technique:
            self.metrics['summary']['mitre_mappings'] += 1
        
        # Recalculate averages
        self._update_averages()
        
        # Save to disk
        self._save_metrics()
        
        return query_id
    
    def _update_averages(self):
        """Update summary averages"""
        queries = self.metrics['queries']
        
        if queries:
            # Average generation time
            total_time = sum(q.get('generation_time_ms', 0) for q in queries)
            self.metrics['summary']['average_generation_time'] = round(
                total_time / len(queries), 2
            )
            
            # Average validation score (percentage of valid queries)
            valid_queries = sum(1 for q in queries if q.get('validation', {}).get('valid', False))
            self.metrics['summary']['average_validation_score'] = round(
                (valid_queries / len(queries)) * 100, 2
            )
    
    def get_summary(self) -> Dict[str, Any]:
        """Get metrics summary"""
        return self.metrics['summary']
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get most recent queries"""
        queries = self.metrics['queries']
        return queries[-limit:] if queries else []
    
    def get_query_by_id(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific query by ID"""
        for query in self.metrics['queries']:
            if query.get('id') == query_id:
                return query
        return None
    
    def get_queries_by_timerange(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict[str, Any]]:
        """Get queries within a time range"""
        results = []
        
        for query in self.metrics['queries']:
            query_time = datetime.fromisoformat(query.get('timestamp'))
            if start_time <= query_time <= end_time:
                results.append(query)
        
        return results
    
    def get_performance_analytics(self) -> Dict[str, Any]:
        """Get detailed performance analytics"""
        queries = self.metrics['queries']
        
        if not queries:
            return {
                'total_queries': 0,
                'success_rate': 0,
                'average_generation_time_ms': 0,
                'validation_rate': 0,
                'query_type_distribution': {},
                'mitre_mapping_rate': 0,
                'error_distribution': {}
            }
        
        total = len(queries)
        successful = sum(1 for q in queries if q.get('success', False))
        valid = sum(1 for q in queries if q.get('validation', {}).get('valid', False))
        with_mitre = sum(1 for q in queries if q.get('mitre_technique'))
        
        # Generation time stats
        gen_times = [q.get('generation_time_ms', 0) for q in queries]
        
        # Query type distribution
        query_types = {}
        for q in queries:
            qtype = q.get('query_type', 'unknown')
            query_types[qtype] = query_types.get(qtype, 0) + 1
        
        # Error distribution
        error_types = {}
        for q in queries:
            if not q.get('success', False):
                error = q.get('error', 'Unknown error')
                # Get first line of error for categorization
                error_category = error.split('\n')[0][:50]
                error_types[error_category] = error_types.get(error_category, 0) + 1
        
        return {
            'total_queries': total,
            'success_rate': round((successful / total) * 100, 2),
            'average_generation_time_ms': round(sum(gen_times) / total, 2),
            'min_generation_time_ms': min(gen_times),
            'max_generation_time_ms': max(gen_times),
            'validation_rate': round((valid / total) * 100, 2),
            'query_type_distribution': query_types,
            'mitre_mapping_rate': round((with_mitre / total) * 100, 2),
            'error_distribution': error_types
        }
    
    def get_time_series_data(self, interval: str = 'hour') -> Dict[str, Any]:
        """Get time series data for visualization"""
        queries = self.metrics['queries']
        
        if not queries:
            return {'timestamps': [], 'counts': [], 'success_counts': []}
        
        # Group queries by time interval
        time_groups = {}
        
        for query in queries:
            timestamp = datetime.fromisoformat(query.get('timestamp'))
            
            if interval == 'hour':
                key = timestamp.strftime('%Y-%m-%d %H:00')
            elif interval == 'day':
                key = timestamp.strftime('%Y-%m-%d')
            elif interval == 'week':
                key = timestamp.strftime('%Y-W%W')
            else:
                key = timestamp.strftime('%Y-%m')
            
            if key not in time_groups:
                time_groups[key] = {'total': 0, 'success': 0}
            
            time_groups[key]['total'] += 1
            if query.get('success', False):
                time_groups[key]['success'] += 1
        
        # Sort by timestamp
        sorted_keys = sorted(time_groups.keys())
        
        return {
            'timestamps': sorted_keys,
            'counts': [time_groups[k]['total'] for k in sorted_keys],
            'success_counts': [time_groups[k]['success'] for k in sorted_keys]
        }
    
    def export_metrics(self, filepath: str):
        """Export metrics to a file"""
        try:
            with open(filepath, 'w') as f:
                json.dump(self.metrics, f, indent=2)
            return True
        except Exception as e:
            print(f"Error exporting metrics: {e}")
            return False
    
    def clear_old_metrics(self, days: int = 30):
        """Clear metrics older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        filtered_queries = [
            q for q in self.metrics['queries']
            if datetime.fromisoformat(q.get('timestamp')) > cutoff_date
        ]
        
        removed_count = len(self.metrics['queries']) - len(filtered_queries)
        self.metrics['queries'] = filtered_queries
        
        # Recalculate summary
        self._update_averages()
        self._save_metrics()
        
        return removed_count


class AnalystFeedback:
    """Tracks analyst feedback and satisfaction"""
    
    def __init__(self, storage_dir: str = None):
        if storage_dir is None:
            storage_dir = os.path.join(os.path.dirname(__file__), '..', 'metrics_data')
        
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        
        self.feedback_file = self.storage_dir / 'feedback.json'
        self.feedback_data = self._load_feedback()
    
    def _load_feedback(self) -> Dict[str, Any]:
        """Load feedback from storage"""
        if self.feedback_file.exists():
            try:
                with open(self.feedback_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {'feedback': [], 'summary': {}}
        return {'feedback': [], 'summary': {}}
    
    def _save_feedback(self):
        """Save feedback to storage"""
        try:
            with open(self.feedback_file, 'w') as f:
                json.dump(self.feedback_data, f, indent=2)
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
    def record_feedback(
        self,
        query_id: str,
        rating: int,
        usefulness: int,
        accuracy: int,
        comments: str = ""
    ) -> bool:
        """Record analyst feedback"""
        
        feedback_entry = {
            'id': f"feedback_{int(time.time() * 1000)}",
            'timestamp': datetime.now().isoformat(),
            'query_id': query_id,
            'rating': rating,  # 1-5
            'usefulness': usefulness,  # 1-5
            'accuracy': accuracy,  # 1-5
            'comments': comments
        }
        
        self.feedback_data['feedback'].append(feedback_entry)
        self._update_feedback_summary()
        self._save_feedback()
        
        return True
    
    def _update_feedback_summary(self):
        """Update feedback summary statistics"""
        feedback = self.feedback_data['feedback']
        
        if not feedback:
            self.feedback_data['summary'] = {}
            return
        
        total = len(feedback)
        
        avg_rating = sum(f.get('rating', 0) for f in feedback) / total
        avg_usefulness = sum(f.get('usefulness', 0) for f in feedback) / total
        avg_accuracy = sum(f.get('accuracy', 0) for f in feedback) / total
        
        self.feedback_data['summary'] = {
            'total_feedback': total,
            'average_rating': round(avg_rating, 2),
            'average_usefulness': round(avg_usefulness, 2),
            'average_accuracy': round(avg_accuracy, 2),
            'satisfaction_score': round((avg_rating / 5) * 100, 2)
        }
    
    def get_feedback_summary(self) -> Dict[str, Any]:
        """Get feedback summary"""
        return self.feedback_data.get('summary', {})
    
    def get_feedback_for_query(self, query_id: str) -> List[Dict[str, Any]]:
        """Get all feedback for a specific query"""
        return[
            f for f in self.feedback_data['feedback']
            if f.get('query_id') == query_id
        ]
