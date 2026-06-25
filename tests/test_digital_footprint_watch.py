from datetime import datetime
from digital_footprint_watch import DigitalFootprintWatch, Alert, Severity
import pytest

def test_add_alert():
    watch = DigitalFootprintWatch()
    alert = Alert("Test alert", datetime.now(), Severity.CRITICAL, "GitHub")
    watch.add_alert(alert)
    assert len(watch.get_alerts()) == 1

def test_get_alerts():
    watch = DigitalFootprintWatch()
    alert1 = Alert("Test alert 1", datetime.now(), Severity.CRITICAL, "GitHub")
    alert2 = Alert("Test alert 2", datetime.now(), Severity.HIGH, "Twitter")
    watch.add_alert(alert1)
    watch.add_alert(alert2)
    assert len(watch.get_alerts()) == 2

def test_get_alerts_by_platform():
    watch = DigitalFootprintWatch()
    alert1 = Alert("Test alert 1", datetime.now(), Severity.CRITICAL, "GitHub")
    alert2 = Alert("Test alert 2", datetime.now(), Severity.HIGH, "Twitter")
    watch.add_alert(alert1)
    watch.add_alert(alert2)
    assert len(watch.get_alerts("GitHub")) == 1

def test_group_alerts_by_severity():
    watch = DigitalFootprintWatch()
    alert1 = Alert("Test alert 1", datetime.now(), Severity.CRITICAL, "GitHub")
    alert2 = Alert("Test alert 2", datetime.now(), Severity.HIGH, "Twitter")
    alert3 = Alert("Test alert 3", datetime.now(), Severity.CRITICAL, "GitHub")
    watch.add_alert(alert1)
    watch.add_alert(alert2)
    watch.add_alert(alert3)
    grouped_alerts = watch.group_alerts_by_severity()
    assert len(grouped_alerts[Severity.CRITICAL]) == 2
    assert len(grouped_alerts[Severity.HIGH]) == 1

def test_filter_alerts():
    watch = DigitalFootprintWatch()
    alert1 = Alert("Test alert 1", datetime.now(), Severity.CRITICAL, "GitHub")
    alert2 = Alert("Test alert 2", datetime.now(), Severity.HIGH, "Twitter")
    alert3 = Alert("Test alert 3", datetime.now(), Severity.CRITICAL, "GitHub")
    watch.add_alert(alert1)
    watch.add_alert(alert2)
    watch.add_alert(alert3)
    filtered_alerts = watch.filter_alerts("GitHub")
    assert len(filtered_alerts) == 2
