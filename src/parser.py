"""
src/parser.py
"""
from bs4 import BeautifulSoup, Tag


def parser(html: str) -> tuple[str, Tag | None, Tag | None]:
    """
    Parse the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text
    heading = soup.find("h1")
    paragraph = soup.find("p")

    return title, heading, paragraph