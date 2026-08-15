"""
main.py
"""
from validators import normalize_url


def main():
    """
    Control the project
    """
    url = input("Enter a website URL: ")
    url = normalize_url(url)
    print(url)


if __name__ == "__main__":
    main()
