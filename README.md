
Web Contact Extractor
=====================

A Python application that extracts contact information such as email addresses, phone numbers, and social media links from a website and saves the results to an Excel spreadsheet.

FEATURES
--------

- URL normalization and validation — removes surrounding whitespace, adds HTTPS when no HTTP/HTTPS scheme is provided, and checks basic URL validity.
- Website downloading — sends HTTP GET requests to retrieve website HTML.
- HTML parsing — parses HTML using BeautifulSoup.
- Email extraction — finds email addresses in visible page text.
- Phone number extraction — identifies potential phone numbers using regular expressions.
- Social media detection — identifies links associated with platforms such as Instagram, Facebook, X, LinkedIn, Telegram, YouTube, TikTok, Threads, Pinterest, Snapchat, WhatsApp, Discord, and Reddit.
- Excel export — saves extracted contacts to an Excel workbook.
- Duplicate prevention — avoids adding contact records that already exist in the spreadsheet.
- Automated tests — includes pytest tests for the main application modules.
- Telegram bot — allows users to submit website URLs through Telegram and receive extracted contacts as an Excel file.
- Deep crawling — provides a command to toggle crawling of selected contact and about pages.

TECHNOLOGIES
------------

- Python
- Requests
- Beautiful Soup 4
- OpenPyXL
- pytest
- python-dotenv
- python-telegram-bot

PROJECT STRUCTURE
-----------------

web-contact-extractor/
|
|-- output/
|   |-- contacts.xlsx
|
|-- src/
|   |-- __init__.py
|   |-- bot.py
|   |-- crawler.py
|   |-- downloader.py
|   |-- excel.py
|   |-- extractor.py
|   |-- main.py
|   |-- parser.py
|   |-- validators.py
|
|-- tests/
|   |-- test_downloader.py
|   |-- test_excel.py
|   |-- test_extractor.py
|   |-- test_parser.py
|   |-- test_validators.py
|
|-- .gitignore
|-- README.md
|-- requirements.txt


INSTALLATION
------------

1. Clone the repository

git clone https://github.com/ManiLashgari/Web-contact-extractor
cd web-contact-extractor

2. Create a virtual environment

python -m venv .venv

Activate it using the command for your operating system.

Windows:

.venv\Scripts\activate

macOS / Linux:

source .venv/bin/activate

3. Install dependencies

pip install -r requirements.txt


USAGE
-----

The Web Contact Extractor can be used in two ways:

- Command-line interface (CLI)
- Telegram bot


1. COMMAND-LINE INTERFACE
-------------------------

Run the application from the project's root directory:

python src/main.py

The application prompts you to enter a website URL:

Enter a website URL: example.com

It then normalizes and validates the URL, downloads the page, parses its HTML, extracts contact information and links, and saves the collected contacts to an Excel file.

The application prints intermediate results, including the normalized URL, extracted emails, phone numbers, links, social media links, and the final contact dictionary.


2. TELEGRAM BOT
---------------

The project also provides a Telegram bot that allows users to extract contact information by sending website URLs directly through Telegram.

Configure the bot
-----------------

Before running the bot, create a .env file in the project's root directory and add your Telegram bot token:

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

Replace your_telegram_bot_token with the token provided by BotFather:

https://t.me/BotFather

Start the bot
-------------

Run the bot from the project's root directory:

python src/bot.py

Open your bot in Telegram and send the /start command.

The bot will send a welcome message asking you to provide a website URL. It also explains how to use the /deep command.

Extract contacts
----------------

Send a website URL to the bot, for example:

example.com

The bot will:

1. Normalize and validate the submitted URL.
2. Download the website HTML.
3. Parse the HTML using BeautifulSoup.
4. Extract email addresses and phone numbers.
5. Extract website links and identify social media links.
6. Save the extracted contacts to an Excel workbook.
7. Send a summary of the extraction results and the Excel file directly to the Telegram chat.

If the URL is invalid or the website HTML cannot be retrieved, the bot sends an error message.

Deep crawling
-------------

By default, the bot extracts contacts from the submitted website page.

You can use the /deep command to enable or disable deep crawling:

/deep

The bot responds with the current deep-crawling status:

- ON — deep crawling is enabled.
- OFF — deep crawling is disabled.

The setting is stored separately for each user, so each user can control their own deep-crawling preference.

When enabled, the bot can check selected internal pages, such as contact and about pages, in addition to the submitted page.

Telegram bot output
------------------

After a successful extraction, the bot sends a summary containing the number of extracted emails, phone numbers, and social media entries.

It also sends the generated Excel workbook directly to the Telegram chat.


OUTPUT
------

The extracted contacts are saved to:

output/contacts.xlsx

The application creates the output directory and workbook when needed. The workbook uses a worksheet named Contacts with the following columns:

URL                    | Type         | Value
-----------------------|--------------|------------------------
https://example.com    | Email        | info@example.com
https://example.com    | Phone number | +1 234 567 8901
https://example.com    | Instagram    | instagram.com/example

These rows are illustrative examples of the output format.

Existing records are checked before new records are appended, helping prevent duplicate entries for the same website, contact type, and value.


FUTURE IMPROVEMENTS
-------------------

- [x] Telegram bot
- [x] Deep crawling


TEAM
----

- [Mani Lashgari](https://github.com/ManiLashgari)

- [Daniyal Iran Mehr](https://github.com/Daniyaliranmehr) (Advisor)
