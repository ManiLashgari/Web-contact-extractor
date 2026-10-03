"""
Tests for the HTML parser.
"""

from bs4 import BeautifulSoup
from src.parser import parser


def test_parser_returns_beautifulsoup():
    """
    Verify that parser returns a BeautifulSoup object.
    """
    html = "<h1>Hello</h1>"

    result = parser(html)

    assert isinstance(result, BeautifulSoup)


def test_parser_parses_html():
    """
    Verify that parser correctly parses HTML elements.
    """
    html = "<h1>Hello</h1><p>World</p>"

    result = parser(html)

    assert result.h1.text == "Hello"
    assert result.p.text == "World"
