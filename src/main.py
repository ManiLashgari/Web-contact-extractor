"""
src/main.py
"""
from validators import normalize_url, is_valid_url
from downloader import url_request


def main():
    """
    Control the project
    """
    url = input("Enter a website URL: ")
    url = normalize_url(url)
    result = is_valid_url(url)
    if not result:
        exit("Invalid URL!")
    url_request(url)


if __name__ == "__main__":
    main()
