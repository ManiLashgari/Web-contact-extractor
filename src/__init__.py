"""
Web contact extractor package.

Provides functions for URL validation and normalization, website
content downloading and parsing, email extraction, and saving
extracted contacts to Excel files.

Exports
-------
normalize_url
    Normalize website URLs.

is_valid_url
    Validate HTTP and HTTPS URLs.

url_request
    Download HTML content from a website.

parser
    Parse HTML content using BeautifulSoup.

extract_email
    Extract email addresses from parsed HTML.

save_contacts
    Save extracted contacts to an Excel file.
"""

from .validators import (
    normalize_url,
    is_valid_url
)

from .downloader import url_request

from .parser import parser

from .extractor import extract_email

from .excel import save_contacts
