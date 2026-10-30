"""
Utilities for downloading HTML content from websites.
"""

import requests


def url_request(url: str) -> str:
    """
    Send an HTTP GET request to a website and return its HTML content.

    Parameters
    ----------
    url : str
        URL of the website to download.

    Returns
    -------
    str or None
        HTML content returned by the server.
        Returns None if a connection error occurs.

    Notes
    -----
    The request uses a timeout of 10 seconds.

    Raises
    ------
    No exceptions are explicitly raised for connection errors.
    A connection error is printed to the console.
    """
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Connection Error!")
    else:
        return response.text
