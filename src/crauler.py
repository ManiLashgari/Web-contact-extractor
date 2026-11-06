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


def _host(url: str) -> str:
    """Return the lowercase host of a URL without a leading ``www.``."""
    host = urlparse(url).netloc.lower()
    return host[4:] if host.startswith("www.") else host


def get_internal_links(base_url: str, parsed_html: str) -> list[str]:
    """
    Collect unique internal links from a parsed page.
 
    Parameters
    ----------
    base_url : str
        Normalized URL of the page the HTML came from. Used to resolve
        relative links and to decide what counts as "internal".
 
    parsed_html : bs4.BeautifulSoup
        Parsed HTML of the page.
 
    Returns
    -------
    list[str]
        Absolute, de-duplicated URLs on the same domain, in page order.
        Fragments, mailto/tel links, and file downloads are excluded.
    """
    base_host = _host(base_url)
    seen = set()
    internal = []

    for tag in parsed_html.find_all("a", href=True):
        href = tag["href"].strip()

        if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        absolute, _ = urldefrag(urljoin(base_url, href))
        parsed = urlparse(absolute)

        if parsed.scheme not in ("http", "https"):
            continue
        if _host(absolute) != base_host:
            continue
        if parsed.path.lower().endswith(SKIP_EXTENSIONS):
            continue

        key = absolute.rstrip("/")
        if key in seen:
            continue

        seen.add(key)
        internal.append(absolute)

    return internal


def select_pages(base_url: str, internal_links: list[str],
                 keywords: tuple=PRIORITY_KEYWORDS, max_pages: int=5) -> list[str]:
    """
    Select internal links likely to contain contact information.
 
    Parameters
    ----------
    base_url : str
        The main page URL. It is never selected again.
 
    internal_links : list[str]
        Links returned by ``get_internal_links``.
 
    keywords : tuple[str, ...]
        A link is selected if its path contains any of these words.
 
    max_pages : int
        Maximum number of pages to select.
 
    Returns
    -------
    list[str]
        Up to ``max_pages`` URLs to crawl.
    """
    base_key = base_url.rstrip("/")
    selected = []

    for link in internal_links:
        if link.rstrip("/") == base_key:
            continue

        path = urlparse(link).path.lower()

        if any(keyword in path for keyword in keywords):
            selected.append(link)

        if len(selected) >= max_pages:
            break

    return selected
