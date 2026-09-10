"""
src/downloader.py
"""
import requests


def url_request(url: str) -> str:
    """
    Request to the URL.
    """
    try:
        response = requests.get(url, timeout=10)
    except requests.exceptions.ConnectionError:
        print("Connection Error!")
    else:
        return response.text
