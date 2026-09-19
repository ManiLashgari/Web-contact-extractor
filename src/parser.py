"""
src/parser.py
"""
from bs4 import BeautifulSoup

def parser(html: str) -> str:
    """
    Parse the HTML.
    """
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.text
    heading = soup.find("h1")
    paragraph = soup.find("p")
    return  title, heading, paragraph
