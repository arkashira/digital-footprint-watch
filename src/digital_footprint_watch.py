import json
from dataclasses import dataclass
from typing import Dict

@dataclass
class Alert:
    repo: str
    file_path: str
    secret: str

class DigitalFootprintWatch:
    def __init__(self, aws_iam_mock):
        self.aws_iam_mock = aws_iam_mock

    def rotate_secret(self, alert: Alert) -> Dict:
        new_secret = self.aws_iam_mock.rotate_access_key(alert.secret)
        return {
            'new_secret': new_secret,
            'commit_message': f'Updated secret in {alert.file_path}'
        }

    def create_commit(self, alert: Alert, new_secret: str) -> str:
        return f'Updated {alert.file_path} with new secret'

    def resolve_alert(self, alert: Alert, new_secret: str) -> str:
        return 'Resolved'

class AWSIAMMock:
    def rotate_access_key(self, secret: str) -> str:
        return f'new_{secret}'

def main():
    aws_iam_mock = AWSIAMMock()
    digital_footprint_watch = DigitalFootprintWatch(aws_iam_mock)
    alert = Alert('repo', 'file_path', 'secret')
    result = digital_footprint_watch.rotate_secret(alert)
    new_commit = digital_footprint_watch.create_commit(alert, result['new_secret'])
    status = digital_footprint_watch.resolve_alert(alert, result['new_secret'])
    print(json.dumps({
        'new_secret': result['new_secret'],
        'commit_message': result['commit_message'],
        'new_commit': new_commit,
        'status': status
    }))

if __name__ == '__main__':
    main()
