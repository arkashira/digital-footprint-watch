import pytest
from digital_footprint_watch import DigitalFootprintWatch, ReputationAnalytics

def test_get_reputation_analytics():
    watch = DigitalFootprintWatch()
    watch.update_reputation_score(60)
    analytics = watch.get_reputation_analytics()
    assert analytics.score == 60
    assert analytics.notifications == []

def test_get_reputation_analytics_low_score():
    watch = DigitalFootprintWatch()
    watch.update_reputation_score(40)
    analytics = watch.get_reputation_analytics()
    assert analytics.score == 40
    assert analytics.notifications == ["Reputation score is low"]

def test_customize_analytics_settings():
    watch = DigitalFootprintWatch()
    watch.customize_analytics_settings(70, "weekly")
    assert watch.analytics_settings["notification_threshold"] == 70
    assert watch.analytics_settings["notification_frequency"] == "weekly"

def test_get_analytics_notifications():
    watch = DigitalFootprintWatch()
    watch.update_reputation_score(40)
    notifications = watch.get_analytics_notifications()
    assert notifications == ["Reputation score is low"]
