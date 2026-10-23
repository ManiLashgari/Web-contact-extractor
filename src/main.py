"""
Main entry point for the web contact extractor application.

Handles user input, URL validation, downloading, parsing,
and processing of website content.
"""

import sys

from parser import parser

from downloader import url_request

from excel import save_contacts

from extractor import (extract_email,
                       extract_phone_number,
                       extract_links,
                       extract_social_media)

from validators import is_valid_url, normalize_url


def main():
    """
    Run the web contact extractor application.

    Prompts the user for a website URL, validates and normalizes
    it, downloads the website content, and parses the HTML.
    """

    url = input("Enter a website URL: ")

    normalized_url = normalize_url(url)

    print("-" * 20, "NORMALIZED URL", "-" * 20)
    print(normalized_url)
    print()

    result = is_valid_url(normalized_url)

    print("-" * 20, "IS VALID URL", "-" * 20)
    print(result)
    print()

    if not result:
        sys.exit("Invalid URL!")

    html = url_request(normalized_url)

    print("-" * 20, "HTML", "-" * 20)
    print(html)
    print()

    parsed_html = parser(html)

    print("-" * 20, "PARSED HTML", "-" * 20)
    print(parsed_html)
    print()

    emails = extract_email(parsed_html)

    print("-" * 20, "ECTRACTED EMAILS", "-" * 20)
    print(emails)
    print()

    phone_numbers = extract_phone_number(parsed_html)

    print("-" * 20, "ECTRACTED PHONE NUMBERS", "-" * 20)
    print(phone_numbers)
    print()

    links = extract_links(parsed_html)

    print("-" * 20, "ECTRACTED LINKS", "-" * 20)
    print(links)
    print()

    social_media = extract_social_media(links)

    print("-" * 20, "ECTRACTED SOCIAL MEDIA", "-" * 20)
    print(social_media)
    print()

    contacts = {"Email": emails,
                "Phone number": phone_numbers,
                **social_media}

    print("-" * 20, "CONTACTS", "-" * 20)
    print(contacts)
    print()

    save_contacts("output/contacts.xlsx", normalized_url, contacts)
    print("THE CONTACTS ARE SAVED.")


if __name__ == "__main__":
    main()
