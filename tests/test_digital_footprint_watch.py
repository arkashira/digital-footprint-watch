from digital_footprint_watch import DigitalFootprintWatch, Alert, AWSIAMMock
import json

def test_rotate_secret():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('repo', 'file_path', 'secret')
    result = digital_footprint_watch.rotate_secret(alert)
    assert result['new_secret'] == 'new_secret'
    assert result['commit_message'] == 'Updated secret in file_path'

def test_create_commit():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('repo', 'file_path', 'secret')
    new_secret = 'new_secret'
    new_commit = digital_footprint_watch.create_commit(alert, new_secret)
    assert new_commit == 'Updated file_path with new secret'

def test_resolve_alert():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('repo', 'file_path', 'secret')
    new_secret = 'new_secret'
    status = digital_footprint_watch.resolve_alert(alert, new_secret)
    assert status == 'Resolved'

def test_rotate_secret_edge_case():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('', '', '')
    result = digital_footprint_watch.rotate_secret(alert)
    assert result['new_secret'] == 'new_'
    assert result['commit_message'] == 'Updated secret in '

def test_main():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('repo', 'file_path', 'secret')
    result = digital_footprint_watch.rotate_secret(alert)
    new_commit = digital_footprint_watch.create_commit(alert, result['new_secret'])
    status = digital_footprint_watch.resolve_alert(alert, result['new_secret'])
    assert json.loads(json.dumps({
        'new_secret': result['new_secret'],
        'commit_message': result['commit_message'],
        'new_commit': new_commit,
        'status': status
    })) == {
        'new_secret': 'new_secret',
        'commit_message': 'Updated secret in file_path',
        'new_commit': 'Updated file_path with new secret',
        'status': 'Resolved'
    }
