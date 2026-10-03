"""
Web contact extractor package.

Provides utilities for validating and normalizing website URLs.
"""

from .validators import (
    normalize_url,
    is_valid_url
)

from .downloader import url_request


from .parser import parser


from .extractor import extract_email
