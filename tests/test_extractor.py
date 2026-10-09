"""
Unit tests for the email extraction utility.
"""

from bs4 import BeautifulSoup

from src.extractor import extract_email


def test_extract_email_returns_single_email():
    """Verify that a single email address is extracted correctly."""
    html = "<p>Contact us at hello@example.com</p>"
    soup = BeautifulSoup(html, "html.parser")

    result = extract_email(soup)

    assert result == ["hello@example.com"]


def test_extract_email_returns_multiple_emails():
    """Verify that multiple email addresses are extracted."""
    html = """
    <p>General: hello@example.com</p>
    <div>Support: support@example.org</div>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_email(soup)

    assert result == [
        "hello@example.com",
        "support@example.org",
    ]


def test_extract_email_returns_empty_list_when_no_emails():
    """Verify that an empty list is returned when no emails are found."""
    html = "<p>Contact us for more information.</p>"
    soup = BeautifulSoup(html, "html.parser")

    result = extract_email(soup)

    assert result == []


def test_extract_email_ignores_html_tags():
    """Verify that email extraction works across different HTML elements."""
    html = """
    <h1>Contact</h1>
    <p>hello@example.com</p>
    <footer>support@example.org</footer>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_email(soup)

    assert result == [
        "hello@example.com",
        "support@example.org",
    ]


def test_extract_email_does_not_match_invalid_addresses():
    """Verify that common malformed email addresses are not extracted."""
    html = """
    <p>Invalid: user@</p>
    <p>Invalid: @example.com</p>
    <p>Valid: hello@example.com</p>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_email(soup)

    assert result == ["hello@example.com"]
