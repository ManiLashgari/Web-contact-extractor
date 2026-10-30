"""
Utilities for parsing HTML documents.
"""

from bs4 import BeautifulSoup


def parser(html: str) -> BeautifulSoup:
    """
    Parse an HTML string into a BeautifulSoup object.

    Parameters
    ----------
    html : str
        HTML content to parse.

    Returns
    -------
    BeautifulSoup
        BeautifulSoup object containing the parsed HTML document.

    Notes
    -----
    Uses Python's built-in ``html.parser`` parser to process
    the HTML content.
    """
    return BeautifulSoup(html, "html.parser")
