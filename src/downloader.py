"""
Utilities for downloading HTML content from websites.
"""

import requests


def url_request(url: str) -> str:
    """
    Send a GET request to a URL and return the response content.

    Args:
        url: The URL to request.

    Returns:
        The HTML content returned by the server.

    Raises:
        requests.exceptions.ConnectionError: If a connection
            to the server cannot be established.
    """
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Connection Error!")
    else:
        return response.text
