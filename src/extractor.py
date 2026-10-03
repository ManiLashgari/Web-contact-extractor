"""
src/extractor.py
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
