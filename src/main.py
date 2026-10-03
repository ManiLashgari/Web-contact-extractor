"""
Main entry point for the web contact extractor application.

Handles user input, URL validation, downloading, parsing,
and processing of website content.
"""

from sys import exit
from parser import parser
from validators import normalize_url, is_valid_url
from downloader import url_request
from extractor import extract_email


def main():
    """
    Run the web contact extractor application.

    Prompts the user for a website URL, validates and normalizes
    it, downloads the website content, and parses the HTML.
    """
    url = input("Enter a website URL: ")
    url = normalize_url(url)
    result = is_valid_url(url)

    if not result:
        exit("Invalid URL!")

    text = url_request(url)
    parsed_text = parser(text)
    print(extract_email(parsed_text))


if __name__ == "__main__":
    main()
