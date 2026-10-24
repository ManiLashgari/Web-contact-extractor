<h1 align="center">Web Contact Extractor</h1>

A Python application that extracts contact information and social media links from a website and saves the results to an Excel spreadsheet.

## Features

- **URL normalization and validation** — removes surrounding whitespace, adds HTTPS when no HTTP/HTTPS scheme is provided, and checks basic URL validity.
- **Website downloading** — sends HTTP GET requests to retrieve website HTML.
- **HTML parsing** — parses HTML using BeautifulSoup.
- **Email extraction** — finds email addresses in visible page text.
- **Phone number extraction** — identifies potential phone numbers using regular expressions.
- **Social media detection** — identifies links associated with platforms such as Instagram, Facebook, X, LinkedIn, Telegram, YouTube, TikTok, Threads, Pinterest, Snapchat, WhatsApp, Discord, and Reddit.
- **Excel export** — saves extracted contacts to an Excel workbook.
- **Duplicate prevention** — avoids adding contact records that already exist in the spreadsheet.
- **Automated tests** — includes pytest tests for the main application modules.

## Technologies

- Python
- Requests
- Beautiful Soup 4
- OpenPyXL
- pytest
- python-dotenv
- python-telegram-bot

## Project Structure

```text
web-contact-extractor/
├── output/
│   └── contacts.xlsx
├── src/
│   ├── __init__.py
│   ├── downloader.py
│   ├── excel.py
│   ├── extractor.py
│   ├── main.py
│   ├── parser.py
│   └── validators.py
├── tests/
│   ├── test_downloader.py
│   ├── test_excel.py
│   ├── test_extractor.py
│   ├── test_parser.py
│   └── test_validators.py
├── .gitignore
├── README.md
├── requirements.txt
└── temp.py
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ManiLashgari/Web-contact-extractor
cd web-contact-extractor
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your operating system.

**Windows:**

```bash
.venv\Scripts\activate
```

**macOS / Linux:**

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

The required packages are specified in `requirements.txt`:

```text
beautifulsoup4==4.15.0
openpyxl==3.1.5
requests==2.28.1
```

To run the tests, install pytest as well if it is not already available:

```bash
pip install pytest
```

## Usage

Run the application from the project's root directory:

```bash
python src/main.py
```

The application prompts you to enter a website URL:

```text
Enter a website URL: example.com
```

It then normalizes and validates the URL, downloads the page, parses its HTML, extracts contact information and links, and saves the collected contacts to an Excel file.

The application prints intermediate results, including the normalized URL, parsed HTML, extracted emails, phone numbers, links, social media links, and the final contact dictionary.

## Output

The extracted contacts are saved to:

```text
output/contacts.xlsx
```

The application creates the output directory and workbook when needed. The workbook uses a worksheet named `Contacts` with the following columns:

| URL | Type | Value |
|---|---|---|
| https://example.com | Email | info@example.com |
| https://example.com | Phone number | +1 234 567 8901 |
| https://example.com | Instagram | instagram.com/example |

These rows are illustrative examples of the output format.

Existing records are checked before new records are appended, helping prevent duplicate entries for the same website, contact type, and value.

## Future Improvements

- [] Telegram bot
- [] Adding support for crawling selected internal pages

## Team

- [Mani Lashgari](https://github.com/ManiLashgari)
- [Daniyal Iran Mehr (Advisor)](https://github.com/Daniyaliranmehr)
