"""
Unit tests for the email extraction utility.
"""

from bs4 import BeautifulSoup

from src.extractor import extract_email, extract_phone_number


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


def make_soup(html: str) -> BeautifulSoup:
    """Parse an HTML string into a BeautifulSoup object."""
    return BeautifulSoup(html, "html.parser")


def test_extracts_international_phone_number():
    """Extract a phone number with an international country code."""
    soup = make_soup("<p>Call us at +1 234 567 8901</p>")

    result = extract_phone_number(soup)

    assert result == ["+1 234 567 8901"]


def test_extracts_phone_number_with_hyphens():
    """Extract a phone number whose parts are separated by hyphens."""
    soup = make_soup("<p>Phone: +44-20-1234-5678</p>")

    result = extract_phone_number(soup)

    assert result == ["+44-20-1234-5678"]


def test_extracts_phone_number_with_parentheses():
    """Extract a phone number containing parentheses."""
    soup = make_soup("<p>Call (123) 456-7890 today</p>")

    result = extract_phone_number(soup)

    assert result == ["(123) 456-7890"]


def test_extracts_phone_number_starting_with_00():
    """Extract a phone number using the 00 international prefix."""
    soup = make_soup("<p>Phone: 0044 20 1234 5678</p>")

    result = extract_phone_number(soup)

    assert result == ["0044 20 1234 5678"]


def test_extracts_multiple_phone_numbers():
    """Extract multiple phone numbers from the same HTML document."""
    soup = make_soup(
        """
        <p>Office: +1 234 567 8901</p>
        <p>Support: (123) 456-7890</p>
        """
    )

    result = extract_phone_number(soup)

    assert result == ["+1 234 567 8901", "(123) 456-7890"]


def test_returns_empty_list_when_no_phone_numbers_exist():
    """Return an empty list when the HTML contains no phone numbers."""
    soup = make_soup("<p>Email us at info@example.com</p>")

    result = extract_phone_number(soup)

    assert result == []


def test_returns_empty_list_for_empty_html():
    """Return an empty list when the HTML document is empty."""
    soup = make_soup("")

    result = extract_phone_number(soup)

    assert result == []


def test_ignores_phone_number_inside_a_word():
    """Do not extract a digit sequence embedded inside a word."""
    soup = make_soup("<p>abc1234567890xyz</p>")

    result = extract_phone_number(soup)

    assert result == []


def test_extracts_phone_numbers_from_combined_html():
    """Extract phone numbers from different HTML elements."""
    soup = make_soup(
        """
        <html>
            <body>
                <h1>Contact Us</h1>
                <p>Phone: +994 50 123 4567</p>
                <div>Alternative: (212) 555-1234</div>
            </body>
        </html>
        """
    )

    result = extract_phone_number(soup)

    assert result == ["+994 50 123 4567", "(212) 555-1234"]
