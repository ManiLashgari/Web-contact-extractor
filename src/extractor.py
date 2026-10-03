"""
src/extractor.py
"""
from bs4 import BeautifulSoup

def extract_email(soup: BeautifulSoup) -> list[str]:
    """
    Extract Email-Adrresses from parsed HTML.
    """
    text = soup.get_text()
