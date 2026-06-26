import json
import os
from unittest.mock import patch, MagicMock
from digital_footprint_watch import UserProfile, authenticate_github, store_refresh_token, get_refresh_token, renew_access_token, sync_repositories

def test_authenticate_github():
    with patch('builtins.input', return_value='dummy_code'):
        with patch('urllib.request.urlopen') as mock_urlopen:
            mock_response = MagicMock()
            mock_response.read.return_value = json.dumps({"access_token": "dummy_token"}).encode('utf-8')
            mock_urlopen.return_value = mock_response
            access_token = authenticate_github()
            assert access_token == "dummy_token"

def test_store_and_get_refresh_token():
    store_refresh_token("dummy_refresh_token")
    refresh_token = get_refresh_token()
    assert refresh_token == "dummy_refresh_token"
    os.remove("refresh_token.txt")

def test_renew_access_token():
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps({"access_token": "new_dummy_token"}).encode('utf-8')
        mock_urlopen.return_value = mock_response
        new_access_token = renew_access_token("dummy_refresh_token")
        assert new_access_token == "new_dummy_token"

def test_sync_repositories():
    user_profile = UserProfile(linked_accounts={})
    with patch('urllib.request.urlopen') as mock_urlopen:
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps([{"name": "repo1"}, {"name": "repo2"}]).encode('utf-8')
        mock_urlopen.return_value = mock_response
        sync_repositories("dummy_access_token", user_profile)
        assert len(user_profile.linked_accounts) == 1
        assert "GitHub" in user_profile.linked_accounts
