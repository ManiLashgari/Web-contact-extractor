from src.validators import is_valid_url, normalize_url


def test_normilize_url():
    assert normalize_url("  example.com ") == "https://example.com"


def test_valid_url():
    assert is_valid_url("https://example.com")


def test_invalid_url_without_domain():
    assert not is_valid_url("https://example")


def test_invalid_url():
    assert not is_valid_url("example")
