"""
validators.py
"""

def normalize_url(url: str) -> str:
    """
    - Normalize a URL by removing surrounding whitespace
    - Adding HTTPS if no sheme is provided
    """
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url