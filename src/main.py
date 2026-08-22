"""
main.py
"""
from validators import normalize_url, is_valid_url


def main():
    """
    Control the project
    """
    url = input("Enter a website URL: ")
    url = normalize_url(url)
    result = is_valid_url(url)
    print(result)


if __name__ == "__main__":
    main()
