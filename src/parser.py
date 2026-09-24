"""
src/parser.py
"""
from bs4 import BeautifulSoup, Tag


def parser(html: str) -> BeautifulSoup:
    """
    Parse the HTML.
    """

    return BeautifulSoup(html, "html.parser")