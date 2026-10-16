"""
Utilities for extracting email addresses from HTML documents.
"""
import re
from bs4 import BeautifulSoup


def extract_email(soup: BeautifulSoup) -> list[str]:
    """
    Extract email addresses from text.

    Args:
        text: Text containing potential email addresses.

    Returns:
        A list of email addresses found in the text.
    """
    text = soup.get_text()

    email_pattern = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"

    return re.findall(email_pattern, text)


def extract_phone_number(soup: BeautifulSoup) -> list[str]:
    """
    Extract potential phone numbers from HTML text.

    Args:
        soup: A BeautifulSoup object containing parsed HTML.

    Returns:
        A list of potential phone numbers found in the text.
    """
    text = soup.get_text(separator=" ", strip=True)

    phone_pattern = (
    r'(?<!\w)(?:\+\d{1,3}|00\d{1,3})[\s.-]?(?:\(?\d{2,4}\)?'
    r'[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?!\w)|(?<!\w)\(?\d{2,4}\)?[\s.-]\d{3,4}[\s.-]\d{3,4}(?!\w)'
    )

    return re.findall(phone_pattern, text)
