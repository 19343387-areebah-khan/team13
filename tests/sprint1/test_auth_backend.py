"""
=============================================================
SPRINT 1 - BACKEND UNIT TESTS
=============================================================
Tests for: Registration & Login (US1 & US2)
Functions tested:
  - validate_username()      (Benjy)
  - validate_email()         (Benjy)
  - validate_password()      (Hamza)
  - hash_password()          (Hamza)
  - compare_password()       (Hamza)
  - check_login_attempts()   (Hamza)
  - sanitize_input()         (Benjy)
  - register_user()          (Benjy)
  - login_user()             (Benjy)
 
Linked Acceptance Criteria:
  - Test 1.2  : Invalid inputs trigger errors
  - Test 1.2b : Mismatched passwords trigger error
  - Test 1.3  : Valid registration redirects to login
  - Test 2.2b : Incorrect credentials trigger error
  - Test 2.3  : Too many failed attempts trigger warning
  - Test 2.4  : Valid credentials redirect to homepage
 
Run with:
  cd C:\\Users\\areeb\\Downloads\\team13
  pytest tests/sprint1/test_auth_backend.py -v
=============================================================
"""
 
import sys
import os
import pytest
from unittest.mock import patch, MagicMock
 
# Add project root to path so imports work
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
 
from utils.security_utils import (
    validate_username,
    validate_email,
    validate_password,
    hash_password,
    compare_password,
    check_login_attempts,
    sanitize_input
)
 
 
# =============================================================
# SANITIZE INPUT TESTS (Benjy)
# =============================================================
 
class TestSanitizeInput:
    """Tests for sanitize_input() - strips whitespace from strings."""
 
    def test_strips_leading_spaces(self):
        """Whitespace before input is removed."""
        assert sanitize_input("  hello") == "hello"
 
    def test_strips_trailing_spaces(self):
        """Whitespace after input is removed."""
        assert sanitize_input("hello  ") == "hello"
 
    def test_strips_both_sides(self):
        """Whitespace on both sides is removed."""
        assert sanitize_input("  hello  ") == "hello"
 
    def test_non_string_returned_as_is(self):
        """Non-string inputs are returned unchanged."""
        assert sanitize_input(None) is None
        assert sanitize_input(123) == 123
 
 
# =============================================================
# USERNAME VALIDATION TESTS (Benjy)
# Linked to: Test 1.2 - Empty or invalid inputs trigger errors
# =============================================================
 
class TestValidateUsername:
    """Tests for validate_username() - checks length and alphanumeric characters."""
 
    def test_valid_username(self):
        """A normal alphanumeric username passes."""
        assert validate_username("areebah") is True
 
    def test_username_too_short(self):
        """Username under 2 characters is rejected."""
        assert validate_username("a") is False
 
    def test_username_too_long(self):
        """Username over 20 characters is rejected."""
        assert validate_username("a" * 21) is False
 
    def test_username_with_special_chars(self):
        """Username with special characters is rejected."""
        assert validate_username("areebah!") is False
 
    def test_username_with_spaces(self):
        """Username with spaces is rejected."""
        assert validate_username("are ebah") is False
 
    def test_empty_username(self):
        """Empty username is rejected."""
        assert validate_username("") is False
 
    def test_none_username(self):
        """None is rejected."""
        assert validate_username(None) is False
 
    def test_username_exactly_2_chars(self):
        """Username of exactly 2 characters passes."""
        assert validate_username("ab") is True
 
    def test_username_exactly_20_chars(self):
        """Username of exactly 20 characters passes."""
        assert validate_username("a" * 20) is True
 
 
# =============================================================
# EMAIL VALIDATION TESTS (Benjy)
# Linked to: Test 1.2 - Empty or invalid inputs trigger errors
# =============================================================
 
class TestValidateEmail:
    """Tests for validate_email() - checks email format using regex."""
 
    def test_valid_email(self):
        """A standard email address passes."""
        assert validate_email("test@test.com") is True
 
    def test_valid_email_with_dots(self):
        """An email with dots in the username passes."""
        assert validate_email("areebah.khan@gmail.com") is True
 
    def test_missing_at_symbol(self):
        """Email without @ is rejected."""
        assert validate_email("testtest.com") is False
 
    def test_missing_domain(self):
        """Email without domain is rejected."""
        assert validate_email("test@") is False
 
    def test_missing_extension(self):
        """Email without .com/.co.uk etc is rejected."""
        assert validate_email("test@test") is False
 
    def test_empty_email(self):
        """Empty string is rejected."""
        assert validate_email("") is False
 
 
# =============================================================
# PASSWORD VALIDATION TESTS (Hamza)
# Linked to: Test 1.2 - Invalid inputs trigger errors
# =============================================================
 
class TestValidatePassword:
    """Tests for validate_password() - checks password strength requirements."""
 
    def test_valid_password(self):
        """A strong password that meets all requirements passes."""
        valid, msg = validate_password("Test@1234")
        assert valid is True
 
    def test_password_too_short(self):
        """Password under 8 characters is rejected."""
        valid, msg = validate_password("Ab1!")
        assert valid is False
        assert "8 characters" in msg
 
    def test_missing_uppercase(self):
        """Password without uppercase letter is rejected."""
        valid, msg = validate_password("test@1234")
        assert valid is False
        assert "uppercase" in msg
 
    def test_missing_lowercase(self):
        """Password without lowercase letter is rejected."""
        valid, msg = validate_password("TEST@1234")
        assert valid is False
        assert "lowercase" in msg
 
    def test_missing_number(self):
        """Password without a number is rejected."""
        valid, msg = validate_password("Test@abcd")
        assert valid is False
        assert "number" in msg
 
    def test_missing_special_character(self):
        """Password without a special character is rejected."""
        valid, msg = validate_password("Test1234")
        assert valid is False
        assert "special" in msg
 
    def test_empty_password(self):
        """Empty password is rejected."""
        valid, msg = validate_password("")
        assert valid is False
 
    def test_none_password(self):
        """None password is rejected."""
        valid, msg = validate_password(None)
        assert valid is False
 
 
# =============================================================
# PASSWORD HASHING TESTS (Hamza)
# Linked to: Test 1.3 - Valid registration stores hashed password
# =============================================================
 
class TestHashPassword:
    """Tests for hash_password() and compare_password()."""
 
    def test_hash_is_not_plaintext(self):
        """Hashed password should not equal the original password."""
        hashed = hash_password("Test@1234")
        assert hashed != "Test@1234"
 
    def test_correct_password_matches_hash(self):
        """The correct password matches against its hash."""
        hashed = hash_password("Test@1234")
        assert compare_password("Test@1234", hashed) is True
 
    def test_wrong_password_does_not_match(self):
        """An incorrect password does not match the hash."""
        hashed = hash_password("Test@1234")
        assert compare_password("WrongPass@1", hashed) is False
 
    def test_two_hashes_of_same_password_differ(self):
        """Hashing the same password twice produces different hashes (salt)."""
        hash1 = hash_password("Test@1234")
        hash2 = hash_password("Test@1234")
        assert hash1 != hash2
 
 
# =============================================================
# LOGIN ATTEMPT PROTECTION TESTS (Hamza)
# Linked to: Test 2.3 - Too many failed attempts trigger warning
# =============================================================
 
class TestCheckLoginAttempts:
    """Tests for check_login_attempts() - locks account after 5 failed attempts."""
 
    def test_below_limit_not_locked(self):
        """User with 4 failed attempts is not locked."""
        user = {"failed_attempts": 4}
        assert check_login_attempts(user) is False
 
    def test_at_limit_is_locked(self):
        """User with exactly 5 failed attempts is locked."""
        user = {"failed_attempts": 5}
        assert check_login_attempts(user) is True
 
    def test_above_limit_is_locked(self):
        """User with more than 5 failed attempts is locked."""
        user = {"failed_attempts": 10}
        assert check_login_attempts(user) is True
 
    def test_zero_attempts_not_locked(self):
        """New user with 0 failed attempts is not locked."""
        user = {"failed_attempts": 0}
        assert check_login_attempts(user) is False
 
 
# =============================================================
# REGISTER USER INTEGRATION TESTS (Benjy)
# Linked to: Test 1.2, Test 1.3
# =============================================================
 
class TestRegisterUser:
    """Tests for register_user() - full registration flow with mocked DB."""
 
    @patch('services.auth_service.get_user_by_username', return_value=None)
    @patch('services.auth_service.get_user_by_email', return_value=None)
    @patch('services.auth_service.add_user', return_value=None)
    def test_valid_registration_succeeds(self, mock_add, mock_email, mock_username):
        """Valid data with unique username and email registers successfully."""
        from services.auth_service import register_user
        result = register_user({
            "username": "areebah",
            "email": "areebah@test.com",
            "password": "Test@1234"
        })
        assert result["success"] is True
 
    def test_invalid_username_rejected(self):
        """Registration with invalid username returns an error."""
        from services.auth_service import register_user
        result = register_user({
            "username": "a",
            "email": "test@test.com",
            "password": "Test@1234"
        })
        assert result["success"] is False
        assert "username" in result["error"].lower()
 
    def test_invalid_email_rejected(self):
        """Registration with invalid email returns an error."""
        from services.auth_service import register_user
        result = register_user({
            "username": "areebah",
            "email": "notanemail",
            "password": "Test@1234"
        })
        assert result["success"] is False
        assert "email" in result["error"].lower()
 
    def test_weak_password_rejected(self):
        """Registration with a weak password returns an error."""
        from services.auth_service import register_user
        result = register_user({
            "username": "areebah",
            "email": "test@test.com",
            "password": "weak"
        })
        assert result["success"] is False
 
    @patch('services.auth_service.get_user_by_username', return_value={"username": "areebah"})
    def test_duplicate_username_rejected(self, mock_username):
        """Registration with a taken username returns an error."""
        from services.auth_service import register_user
        result = register_user({
            "username": "areebah",
            "email": "new@test.com",
            "password": "Test@1234"
        })
        assert result["success"] is False
        assert "username" in result["error"].lower()
 
    @patch('services.auth_service.get_user_by_username', return_value=None)
    @patch('services.auth_service.get_user_by_email', return_value={"email": "taken@test.com"})
    def test_duplicate_email_rejected(self, mock_email, mock_username):
        """Registration with a taken email returns an error."""
        from services.auth_service import register_user
        result = register_user({
            "username": "newuser",
            "email": "taken@test.com",
            "password": "Test@1234"
        })
        assert result["success"] is False
        assert "email" in result["error"].lower()
 
 
# =============================================================
# LOGIN USER INTEGRATION TESTS (Benjy/Hamza)
# Linked to: Test 2.2b, Test 2.3, Test 2.4
# =============================================================
 
class TestLoginUser:
    """Tests for login_user() - full login flow with mocked DB."""
 
    def _make_user(self, password="Test@1234", failed_attempts=0):
        """Helper to create a mock user dict."""
        return {
            "user_id": 1,
            "username": "areebah",
            "email": "test@test.com",
            "password_hash": hash_password(password),
            "failed_attempts": failed_attempts
        }
 
    @patch('services.auth_service.reset_failed_attempts')
    @patch('services.auth_service.get_user_by_email')
    def test_valid_login_succeeds(self, mock_get_user, mock_reset):
        """Correct credentials return success and user_id."""
        mock_get_user.return_value = self._make_user()
        from services.auth_service import login_user
        result = login_user({"email": "test@test.com", "password": "Test@1234"})
        assert result["success"] is True
        assert "user_id" in result
 
    @patch('services.auth_service.get_user_by_email', return_value=None)
    def test_nonexistent_email_rejected(self, mock_get_user):
        """Login with an email that doesn't exist returns error."""
        from services.auth_service import login_user
        result = login_user({"email": "nobody@test.com", "password": "Test@1234"})
        assert result["success"] is False
        assert "credentials" in result["error"].lower()
 
    @patch('services.auth_service.update_failed_attempts')
    @patch('services.auth_service.get_user_by_email')
    def test_wrong_password_rejected(self, mock_get_user, mock_update):
        """Incorrect password returns invalid credentials error."""
        mock_get_user.return_value = self._make_user()
        from services.auth_service import login_user
        result = login_user({"email": "test@test.com", "password": "WrongPass@1"})
        assert result["success"] is False
        assert "credentials" in result["error"].lower()
 
    @patch('services.auth_service.get_user_by_email')
    def test_locked_account_rejected(self, mock_get_user):
        """Account with 5+ failed attempts is locked."""
        mock_get_user.return_value = self._make_user(failed_attempts=5)
        from services.auth_service import login_user
        result = login_user({"email": "test@test.com", "password": "Test@1234"})
        assert result["success"] is False
        assert "locked" in result["error"].lower()
        