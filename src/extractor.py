"""
Utilities for extracting contact information, website links, and
social media links from HTML documents.
"""

import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

SOCIAL_MEDIA_DOMAINS = {
    "Instagram": ["instagram.com"],
    "Facebook": ["facebook.com", "fb.com", "fb.me"],
    "X": ["x.com", "twitter.com"],
    "LinkedIn": ["linkedin.com"],
    "Telegram": ["t.me", "telegram.me"],
    "YouTube": ["youtube.com", "youtu.be"],
    "TikTok": ["tiktok.com"],
    "Threads": ["threads.net"],
    "Pinterest": ["pinterest.com"],
    "Snapchat": ["snapchat.com"],
    "WhatsApp": ["whatsapp.com", "wa.me"],
    "Discord": ["discord.com", "discord.gg"],
    "Reddit": ["reddit.com"],
}


def extract_email(soup: BeautifulSoup) -> list[str]:
    """
    Extract email addresses from the text content of an HTML document.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object containing the parsed HTML document.

    Returns
    -------
    list[str]
        List of email addresses found in the document's text content.

    Notes
    -----
    Email addresses are identified using a regular expression.
    Only text extracted through BeautifulSoup's get_text() method
    is searched.
    """
    text = soup.get_text(separator=" ", strip=True)

    email_pattern = r"[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+"

    return re.findall(email_pattern, text)


def extract_phone_number(soup: BeautifulSoup) -> list[str]:
    """
    Extract potential phone numbers from an HTML document.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object containing the parsed HTML document.

    Returns
    -------
    list[str]
        List of potential phone numbers found in the document's
        text content.

    Notes
    -----
    Phone numbers are identified using a regular expression that
    supports several international and local number formats.
    The extracted numbers are not independently validated.
    """
    text = soup.get_text(separator=" ", strip=True)

    phone_pattern = (
    r'(?<!\w)(?:\+\d{1,3}|00\d{1,3})[\s.-]?(?:\(?\d{2,4}\)?'
    r'[\s.-]?)?\d{3,4}[\s.-]?\d{3,4}(?!\w)|(?<!\w)\(?\d{2,4}\)?[\s.-]\d{3,4}[\s.-]\d{3,4}(?!\w)'
    )

    return re.findall(phone_pattern, text)


def extract_links(soup: BeautifulSoup) -> list[str]:
    """
    Extract hyperlink URLs from HTML anchor tags.

    Parameters
    ----------
    soup : BeautifulSoup
        BeautifulSoup object containing the parsed HTML document.

    Returns
    -------
    list[str]
        List of href attribute values from anchor tags.
        Anchor tags without an href attribute are ignored.
    """
    links = []
    for tag in soup.find_all("a", href=True):
        links.append(tag["href"])

    return links


def extract_social_media(links_list: list[str]) -> dict[str, list[str]]:
    """
    Identify social media links from a list of URLs.

    Parameters
    ----------
    links_list : list[str]
        List of URLs to check for supported social media domains.

    Returns
    -------
    dict[str, list[str]]
        Dictionary mapping recognized social media platform names
        to lists containing their corresponding hostnames and paths.

    Notes
    -----
    Supported platforms include Instagram, Facebook, X, LinkedIn,
    Telegram, YouTube, TikTok, Threads, Pinterest, Snapchat,
    WhatsApp, Discord, and Reddit.

    Domain matching supports the configured domains and their
    subdomains. The extracted values contain the hostname and path
    without the URL scheme or query parameters.
    """
    social_media = {}

    for link in links_list:

        parsed_link = urlparse(link)
        netloc = parsed_link.netloc.lower().removeprefix("www.")

        for platform, domains in SOCIAL_MEDIA_DOMAINS.items():

            for domain in domains:

                if domain == netloc or netloc.endswith("." + domain):
                    social_media[platform] = []
                    item = parsed_link.netloc + parsed_link.path

                    if item not in social_media[platform]:
                        social_media[platform].append(item)

                    break

            else:
                continue

            break

    return social_media
