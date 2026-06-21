class EmailService:
    def __init__(self):
        self.sent_emails = []

    def send_confirmation(self, email: str, token: str):
        # In a real system this would send an email.
        # Here we just record the action.
        self.sent_emails.append((email, token))
