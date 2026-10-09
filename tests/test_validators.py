"""
Unit tests for URL validation and normalization utilities.
"""

from src.validators import is_valid_url, normalize_url


def test_normalize_url():
    """
    Verify that whitespace is removed and HTTPS is added.
    """
    assert normalize_url("  example.com ") == "https://example.com"


def test_valid_url():
    """
    Verify that a valid HTTPS URL is accepted.
    """
    assert is_valid_url("https://example.com")


def test_invalid_url_without_domain():
    """
    Verify that a URL without a complete domain is rejected.
    """
    assert not is_valid_url("https://example")


def test_invalid_url():
    """
    Verify that a URL without a scheme is rejected.
    """
    assert not is_valid_url("example")
