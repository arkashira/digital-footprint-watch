from digital_footprint_watch import DigitalFootprintWatch, ReputationAnalytics

def test_get_reputation_analytics():
    watch = DigitalFootprintWatch()
    analytics = watch.get_reputation_analytics()
    assert analytics.score == 75
    assert analytics.notifications == ["Your reputation score is above average"]

def test_customize_analytics_settings():
    watch = DigitalFootprintWatch()
    watch.customize_analytics_settings("weekly", 60)
    assert watch.analytics_settings["notification_frequency"] == "weekly"
    assert watch.analytics_settings["score_threshold"] == 60

def test_get_analytics_notifications_above_threshold():
    watch = DigitalFootprintWatch()
    watch.customize_analytics_settings("daily", 50)
    notifications = watch.get_analytics_notifications()
    assert notifications == ["Your reputation score is above average"]

def test_get_analytics_notifications_below_threshold():
    watch = DigitalFootprintWatch()
    watch.customize_analytics_settings("daily", 80)
    notifications = watch.get_analytics_notifications()
    assert notifications == []
