"""
Utilities for parsing HTML documents.
"""

from bs4 import BeautifulSoup


def parser(html: str) -> BeautifulSoup:
    """
    Parse an HTML string into a BeautifulSoup object.

    Args:
        html: The HTML content to parse.

    Returns:
        A BeautifulSoup object containing the parsed HTML document.
    """
    return BeautifulSoup(html, "html.parser")
