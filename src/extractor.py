"""
Utilities for extracting email addresses from HTML documents.
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
    Extract email addresses from text.

    Args:
        text: Text containing potential email addresses.

    Returns:
        A list of email addresses found in the text.
    """
    text = soup.get_text(separator=" ", strip=True)

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


def extract_links(soup: BeautifulSoup) -> list[str]:
    """
    Extract the link of all <a> tags.
    """
    links = []
    for tag in soup.find_all("a", href=True):
        links.append(tag["href"])

    return links


def extract_social_media(links_list: list[str]) -> dict[str, list[str]]:
    """
        Extract social media from HTML text.
    
        Args:
            soup: A BeautifulSoup object containing parsed HTML.
    
        Returns:
            A list of potential social media found in the text.
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
