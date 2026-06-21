from .user_store import UserStore
from .email_service import EmailService

class Platform:
    def __init__(self):
        self.store = UserStore()
        self.email_service = EmailService()

    def sign_up(self, email: str, password: str) -> str:
        user = self.store.add_user(email, password)
        self.email_service.send_confirmation(email, user.confirmation_token)
        return user.confirmation_token

    def confirm_email(self, token: str) -> bool:
        return self.store.confirm(token)

    def login(self, email: str, password: str) -> bool:
        return self.store.authenticate(email, password)
