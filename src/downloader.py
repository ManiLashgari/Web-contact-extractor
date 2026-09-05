"""
src/downloader.py
"""
import requests

try:
    response = requests.get("https://asdghj.com", timeout=10,)
except requests.exceptions.ConnectionError:
    print("Connection Error!")
else:
    print(response)
    print("-" * 10, "STATUS CODE", "-" * 10)
    print(response.status_code)
    print("-" * 10, "HEADERS", "-" * 10)
    print(response.headers)
    print("-" * 10, "TEXT", "-" * 10)
    print(response.text)
    print(f"TYPE: {type(response.text)}")
    print("-" * 10, "CONTENT", "-" * 10)
    print(response.content)
    print(f"TYPE: {type(response.content)}")
