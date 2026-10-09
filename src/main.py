"""
Main entry point for the web contact extractor application.

Handles user input, URL validation, downloading, parsing,
and processing of website content.
"""

import sys

from parser import parser

from downloader import url_request

from excel import save_contacts

from extractor import extract_email

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

    data = extract_email(parsed_html)

    print("-" * 20, "ECTRACTED EMAILS", "-" * 20)
    print(data)
    print()

    save_contacts("output/contacts.xlsx", normalized_url, data)
    print("THE CONTACTS ARE SAVED.")


if __name__ == "__main__":
    main()
