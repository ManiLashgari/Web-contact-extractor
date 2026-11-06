import time
from urllib.parse import urljoin, urlparse, urldefrag
from parser import parser
from downloader import url_request

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


def get_internal_links(base_url: str, parsed_html: object) -> list[str]:
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


def crawl_selected_pages(base_url: str, parsed_html: object, max_pages: int=5, delay: int=1.0):
    """
    Download and parse the selected internal pages of a website.
 
    Parameters
    ----------
    base_url : str
        Normalized URL of the main page.
 
    parsed_html : bs4.BeautifulSoup
        Parsed HTML of the main page.
 
    max_pages : int
        Maximum number of internal pages to download.
 
    delay : float
        Seconds to wait before each request, to avoid hammering the site.
 
    Returns
    -------
    list[tuple[str, bs4.BeautifulSoup]]
        ``(page_url, parsed_page)`` for every page downloaded successfully.
    """
    links = get_internal_links(base_url, parsed_html)
    pages = select_pages(base_url, links, max_pages=max_pages)
    print(f"[INFO] Internal pages selected: {pages}")

    results = []

    for page_url in pages:
        time.sleep(delay)
        html = url_request(page_url)

        if not html:
            print(f"[WARNING] Skipping empty page: {page_url}")
            continue

        results.append((page_url, parser(html)))
        print(f"[INFO] Crawled: {page_url}")

    return results


def merge_unique(*lists):
    """Merge lists into one list, removing duplicates and keeping order."""
    merged = []

    for items in lists:
        for item in items:
            if item not in merged:
                merged.append(item)

    return merged


def merge_social_media(target, new):
    """
    Merge a social media dict into another one in place.
 
    Both dicts map a platform name to a list of links.
    """
    for platform, links in new.items():
        target[platform] = merge_unique(target.get(platform, []), links)
