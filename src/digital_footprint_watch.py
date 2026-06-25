from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

class Severity(Enum):
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4

@dataclass
class Alert:
    description: str
    timestamp: datetime
    severity: Severity
    platform: str

class DigitalFootprintWatch:
    def __init__(self):
        self.alerts = []

    def add_alert(self, alert: Alert):
        self.alerts.append(alert)

    def get_alerts(self, platform: str = None):
        if platform:
            return [alert for alert in self.alerts if alert.platform == platform]
        return self.alerts

    def group_alerts_by_severity(self, platform: str = None):
        alerts = self.get_alerts(platform)
        grouped_alerts = {severity: [] for severity in Severity}
        for alert in alerts:
            grouped_alerts[alert.severity].append(alert)
        return grouped_alerts

    def filter_alerts(self, platform: str):
        return [alert for alert in self.alerts if alert.platform == platform]
