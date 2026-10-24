# Web Contact Extractor

A Python application that extracts contact information and social media links from a website and saves the results to an Excel spreadsheet.

## Features

- **URL normalization and validation** — removes surrounding whitespace, adds HTTPS when no HTTP/HTTPS scheme is provided, and checks basic URL validity.
- **Website downloading** — sends HTTP GET requests to retrieve website HTML.
- **HTML parsing** — parses HTML using BeautifulSoup.
- **Email extraction** — finds email addresses in visible page text.
- **Phone number extraction** — identifies potential phone numbers using regular expressions.
- **Link extraction** — collects links from HTML anchor tags.
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
git clone <repository-url>
cd web-contact-extractor
```

Replace `<repository-url>` with the URL of your repository.

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

## Running Tests

Run the test suite from the project root:

```bash
pytest
```

The tests cover:

- URL normalization and validation
- Website request behavior
- HTML parsing
- Email and phone number extraction
- Link and social media extraction
- Excel file creation and contact storage

## Limitations

- **Single-page extraction:** The application processes the URL entered by the user. It does not automatically crawl other pages on the website.
- **Pattern-based extraction:** Email and phone number extraction relies on regular expressions and may miss valid contacts or identify false positives.
- **Visible text:** Email addresses and phone numbers are extracted from text returned by BeautifulSoup's `get_text()` method. Contacts present only in images, scripts, or other non-visible page content may not be found.
- **Basic URL validation:** URL validation checks the HTTP/HTTPS scheme and whether the hostname contains a dot. It does not guarantee that the website exists or is reachable.
- **Network errors:** A connection error is printed by the downloader, which returns `None`. The main application does not currently handle that result before parsing.
- **Social media links:** Social media detection depends on the configured domain list and links found in anchor tags. Multiple different links from the same social platform may not all be preserved in the current implementation.

## Future Improvements

Potential improvements include:

- Better handling of connection errors and HTTP response statuses
- More comprehensive URL validation
- Improved phone number validation
- Preserving multiple links for each social media platform
- Adding command-line arguments instead of interactive input
- Expanding test coverage for error cases and Excel workbook edge cases
- Adding support for crawling selected internal pages

## License

No license has been specified yet. Add a license file if you intend to distribute or reuse this project publicly.
