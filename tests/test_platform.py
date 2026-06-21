import pytest
from platform import Platform

@pytest.fixture
def platform():
    return Platform()

def test_successful_signup_and_login(platform):
    token = platform.sign_up("user@example.com", "secret")
    assert token is not None
    # Email sent
    assert ("user@example.com", token) in platform.email_service.sent_emails
    # Confirm email
    assert platform.confirm_email(token) is True
    # Login succeeds
    assert platform.login("user@example.com", "secret") is True

def test_signup_duplicate_email(platform):
    platform.sign_up("dup@example.com", "pass1")
    with pytest.raises(ValueError, match="Email already registered"):
        platform.sign_up("dup@example.com", "pass2")

def test_login_unconfirmed_user(platform):
    platform.sign_up("unconfirmed@example.com", "pass")
    assert platform.login("unconfirmed@example.com", "pass") is False

def test_login_wrong_password(platform):
    token = platform.sign_up("wrongpass@example.com", "correct")
    platform.confirm_email(token)
    assert platform.login("wrongpass@example.com", "wrong") is False

def test_confirm_invalid_token(platform):
    assert platform.confirm_email("invalid-token") is False
