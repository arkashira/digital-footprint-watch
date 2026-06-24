import json
from dataclasses import dataclass
from typing import List

@dataclass
class ReputationAnalytics:
    score: int
    notifications: List[str]

class DigitalFootprintWatch:
    def __init__(self):
        self.analytics_settings = {
            "notification_frequency": "daily",
            "score_threshold": 50
        }

    def get_reputation_analytics(self) -> ReputationAnalytics:
        # Simulate analytics calculation
        score = 75
        notifications = ["Your reputation score is above average"]
        return ReputationAnalytics(score, notifications)

    def customize_analytics_settings(self, notification_frequency: str, score_threshold: int):
        self.analytics_settings["notification_frequency"] = notification_frequency
        self.analytics_settings["score_threshold"] = score_threshold

    def get_analytics_notifications(self) -> List[str]:
        analytics = self.get_reputation_analytics()
        if analytics.score > self.analytics_settings["score_threshold"]:
            return analytics.notifications
        else:
            return []
