"""
src/validators.py
"""

from urllib.parse import urlparse

def normalize_url(url: str) -> str:
    """
    Normalize a URL by removing surrounding whitespace and adding HTTPS
    if no URL scheme is provided.

    Parameters
    ----------
    url
        URL to normalize.

    Returns
    -------
    str
        Normalized URL with surrounding whitespace removed and an HTTPS
        scheme added if no HTTP or HTTPS scheme is present.
    """
    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return url


def is_valid_url(url: str) -> bool:
    """
    Validate whether a URL has a valid HTTP or HTTPS scheme, hostname and domain.

    Parameters
    ----------
    url
        URL to validate.

    Returns
    -------
    bool
        ``True`` if the URL has an HTTP or HTTPS scheme and a hostname
        containing a dot; otherwise, ``False``.
    """
    parsed_url = urlparse(url)

    return bool(parsed_url.scheme in ("https", "http") \
                and parsed_url.hostname and "." in parsed_url.hostname)
