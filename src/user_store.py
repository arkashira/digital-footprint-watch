import uuid
from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class User:
    email: str
    password: str
    confirmed: bool = False
    confirmation_token: Optional[str] = None

class UserStore:
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._tokens: Dict[str, str] = {}  # token -> email

    def add_user(self, email: str, password: str) -> User:
        if email in self._users:
            raise ValueError("Email already registered")
        token = str(uuid.uuid4())
        user = User(email=email, password=password, confirmation_token=token)
        self._users[email] = user
        self._tokens[token] = email
        return user

    def confirm(self, token: str) -> bool:
        email = self._tokens.pop(token, None)
        if not email:
            return False
        user = self._users[email]
        user.confirmed = True
        user.confirmation_token = None
        return True

    def authenticate(self, email: str, password: str) -> bool:
        user = self._users.get(email)
        if not user or not user.confirmed:
            return False
        return user.password == password
