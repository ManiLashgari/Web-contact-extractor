"""
tess/test_validators.py
"""
from src.validators import is_valid_url, normalize_url


def test_normilize_url():
    """
    Test normilize_url method.
    """
    assert normalize_url("  example.com ") == "https://example.com"


def test_valid_url():
    """
    Test is_valid_url method with valid URL.
    """
    assert is_valid_url("https://example.com")


def test_invalid_url_without_domain():
    """
    Test is_valid_url method with invalid URL without domain.
    """
    assert not is_valid_url("https://example")


def test_invalid_url():
    """
    Test is_valid_url method with invalid URL.
    """
    assert not is_valid_url("example")
