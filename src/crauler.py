import time
from urllib.parse import urljoin, urlparse, urldefrag

PRIORITY_KEYWORDS = (
    "contact",
    "about",
    "team",
    "support",
    "help",
    "reach",
    "connect",
    "location",
    "impressum",
)

SKIP_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
    ".zip", ".rar", ".mp3", ".mp4", ".doc", ".docx", ".xls", ".xlsx",
)


def _host(url):
    """Return the lowercase host of a URL without a leading ``www.``."""
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host
