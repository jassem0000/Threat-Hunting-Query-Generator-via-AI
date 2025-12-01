"""
Real-time notification system using file-based change detection
This allows the dashboard to detect when new queries are generated without constant polling
"""
import json
import os
from pathlib import Path
from datetime import datetime

class ChangeNotifier:
    """Notify when queries change without using WebSockets"""
    
    def __init__(self, notification_file='backend/query_changes.json'):
        self.notification_file = Path(notification_file)
        self.notification_file.parent.mkdir(exist_ok=True)
        
        # Initialize notification file if not exists
        if not self.notification_file.exists():
            self._write_notification({
                'last_change': None,
                'query_count': 0,
                'last_query_id': None
            })
    
    def _read_notification(self):
        """Read notification state"""
        try:
            with open(self.notification_file, 'r') as f:
                return json.load(f)
        except:
            return {'last_change': None, 'query_count': 0, 'last_query_id': None}
    
    def _write_notification(self, data):
        """Write notification state"""
        try:
            with open(self.notification_file, 'w') as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error writing notification: {e}")
    
    def notify_query_added(self, query_id, query_count):
        """Notify that a new query was added"""
        data = {
            'last_change': datetime.now().isoformat(),
            'query_count': query_count,
            'last_query_id': query_id,
            'change_type': 'query_added'
        }
        self._write_notification(data)
    
    def get_last_change(self):
        """Get last change timestamp"""
        data = self._read_notification()
        return data.get('last_change')
    
    def get_change_info(self):
        """Get full change information"""
        return self._read_notification()
    
    def has_changes_since(self, timestamp):
        """Check if there are changes since given timestamp"""
        last_change = self.get_last_change()
        if last_change is None or timestamp is None:
            return False
        return last_change > timestamp

# Singleton instance
_notifier = None

def get_notifier():
    global _notifier
    if _notifier is None:
        _notifier = ChangeNotifier()
    return _notifier
