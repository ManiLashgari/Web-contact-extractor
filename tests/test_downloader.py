"""
tests/test_downloader.py
"""
from unittest.mock import patch, Mock
import requests

from src.downloader import url_request


@patch("src.downloader.requests.get")
def test_url_request_success(mock_get):
    """
    Test valid URL.
    """
    mock_response = Mock()
    mock_response.text = "Hello, world!"
    mock_get.return_value = mock_response

    result = url_request("https://example.com")

    assert result == "Hello, world!"
    mock_get.assert_called_once_with(
        "https://example.com",
        timeout=10,
    )


@patch("src.downloader.requests.get")
def test_url_request_connection_error(mock_get, capsys):
    """
    Test Connection Error.
    """
    mock_get.side_effect = requests.exceptions.ConnectionError

    result = url_request("https://example.com")

    captured = capsys.readouterr()

    assert result is None
    assert captured.out == "Connection Error!\n"
