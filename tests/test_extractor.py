"""
Unit tests for the email extraction utility.
"""

from bs4 import BeautifulSoup

from src.extractor import extract_email, extract_phone_number, extract_links, extract_social_media


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


def test_extracts_single_link():
    """Extract the href attribute from a single anchor tag."""
    soup = BeautifulSoup(
        '<a href="https://example.com">Example</a>',
        "html.parser",
    )

    result = extract_links(soup)

    assert result == ["https://example.com"]


def test_extracts_multiple_links():
    """Extract href attributes from multiple anchor tags."""
    html = """
    <a href="https://example.com">Example</a>
    <a href="https://google.com">Google</a>
    <a href="/contact">Contact</a>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_links(soup)

    assert result == [
        "https://example.com",
        "https://google.com",
        "/contact",
    ]


def test_ignores_anchor_tags_without_href():
    """Ignore anchor tags that do not have an href attribute."""
    html = """
    <a href="https://example.com">Example</a>
    <a>No link</a>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_links(soup)

    assert result == ["https://example.com"]


def test_returns_empty_list_when_no_links_exist():
    """Return an empty list when the HTML contains no anchor tags."""
    soup = BeautifulSoup("<p>No links here.</p>", "html.parser")

    result = extract_links(soup)

    assert not result


def test_preserves_link_order():
    """Preserve the order in which links appear in the HTML."""
    html = """
    <a href="/first">First</a>
    <a href="/second">Second</a>
    <a href="/third">Third</a>
    """
    soup = BeautifulSoup(html, "html.parser")

    result = extract_links(soup)

    assert result == ["/first", "/second", "/third"]


def test_extracts_instagram_link():
    """Extract an Instagram link from the input list."""
    links = ["https://www.instagram.com/example/"]

    result = extract_social_media(links)

    assert result == {
        "Instagram": ["www.instagram.com/example/"]
    }


def test_extracts_telegram_link():
    """Extract a Telegram link from the input list."""
    links = ["https://t.me/example"]

    result = extract_social_media(links)

    assert result == {
        "Telegram": ["t.me/example"]
    }


def test_extracts_multiple_social_media_platforms():
    """Extract links from multiple social media platforms."""
    links = [
        "https://www.instagram.com/example/",
        "https://t.me/example",
        "https://www.facebook.com/example",
    ]

    result = extract_social_media(links)

    assert result == {
        "Instagram": ["www.instagram.com/example/"],
        "Telegram": ["t.me/example"],
        "Facebook": ["www.facebook.com/example"],
    }


def test_does_not_duplicate_identical_links():
    """Ensure identical links appear only once in the results."""
    links = [
        "https://instagram.com/example",
        "https://instagram.com/example",
    ]

    result = extract_social_media(links)

    assert result == {
        "Instagram": ["instagram.com/example"]
    }


def test_ignores_non_social_media_links():
    """Ignore links whose domains are not recognized social platforms."""
    links = [
        "https://example.com",
        "https://mywebsite.org/contact",
    ]

    result = extract_social_media(links)

    assert not result


def test_returns_empty_dictionary_for_empty_input():
    """Return an empty dictionary when no links are provided."""
    result = extract_social_media([])

    assert not result


def test_matches_subdomains_of_social_media_domains():
    """Recognize a social platform when its domain is a subdomain."""
    links = ["https://m.instagram.com/example"]

    result = extract_social_media(links)

    assert result == {
        "Instagram": ["m.instagram.com/example"]
    }


def test_ignores_domains_that_only_contain_a_social_domain_name():
    """Avoid matching unrelated domains containing a platform's name."""
    links = ["https://notinstagram.com/example"]

    result = extract_social_media(links)

    assert not result
