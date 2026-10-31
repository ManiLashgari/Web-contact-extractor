"""
Telegram bot for extracting contact information from websites.

Provides a Telegram interface for the Web Contact Extractor application.
Users can send website URLs to the bot, which validates and normalizes
the URLs, downloads and parses website HTML, and extracts contact
information.

The extracted information includes:
    - Email addresses
    - Phone numbers
    - Website links
    - Social media links

Extracted contacts are saved to an Excel workbook at
``output/contacts.xlsx``.

The bot uses the python-telegram-bot library to handle incoming
messages and respond to users asynchronously.

Environment Variables
---------------------
TELEGRAM_BOT_TOKEN : str
    Telegram bot token used to authenticate the bot.
    Must be defined in the ``.env`` file.

Dependencies
------------
python-telegram-bot
python-dotenv
requests
beautifulsoup4
openpyxl
"""
import os

from dotenv import load_dotenv

from telegram import Update

from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,
    MessageHandler,
    filters
)

from validators import (
    normalize_url,
    is_valid_url
)

from parser import parser

from downloader import url_request

from excel import save_contacts

from extractor import (extract_email,
                       extract_phone_number,
                       extract_links,
                       extract_social_media)


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Start the Telegram bot and send a welcome message to the user.

    Parameters
    ----------
    update : Update
        Telegram update object containing the incoming command
        and information about the user and chat.

    context : ContextTypes.DEFAULT_TYPE
        Context object containing information and data associated
        with the current update.

    Returns
    -------
    None
        Sends a welcome message asking the user to provide
        a website URL.
    """
    await update.message.reply_text("Hello! Welcome to Web Contact Extractor."
    "\n\nPlease send me a website URL.")


async def handle_message(update: Update, context: ContextTypes):
    """
    Process a website URL sent by the user and extract contact information.

    Normalizes and validates the URL, downloads the website HTML,
    parses its content, extracts email addresses, phone numbers,
    website links, and social media links, and saves the extracted
    contacts to an Excel file.

    Parameters
    ----------
    update : Update
        Telegram update object containing the incoming text message
        and information about the user and chat.

    context : ContextTypes
        Context object containing information and data associated
        with the current update.

    Returns
    -------
    None
        Sends a response to the user with the extraction results.
        Returns early if the URL is invalid, the downloaded HTML
        is empty, or no contacts are found.

    Notes
    -----
    Extracted contacts are saved to ``output/contacts.xlsx``.
    Processing information and errors are printed to the console.
    """
    message = update.message.text
    print(f"[INFO] Recived message: {message}")

    normalized_url = normalize_url(message)
    print(f"[INFO] Normalized URL: {normalized_url}")

    is_valid = is_valid_url(normalized_url)

    if not is_valid:
        await update.message.reply_text("Invalid URL ❌ Please send a valid website URL.")
        print(f"[ERROR] The URL is invalid!: {normalized_url}")
        return

    print(f"[INFO] Valid URL received: {normalized_url}")

    html = url_request(normalized_url)

    if not html:
        await update.message.reply_text("The HTML is empty ❌ Please send another website URL.")
        print("[ERROR] The HTML is empty.")
        return
    print(f"[INFO] The HTML is received. HTML length: {len(html)}")

    parsed_html = parser(html)
    print("[INFO] The HTML is parsed.")

    emails = extract_email(parsed_html)

    if not emails:
        print("[INFO] No email found.")
    else:
        print(f"[INFO] The emails are extracted:\n{emails}")
        print(f"[INFO] The number of emails: {len(emails)}")

    phone_numbers = extract_phone_number(parsed_html)

    if not phone_numbers:
        print("[INFO] No phone number found.")
    else:
        print(f"[INFO] The phone numbers are extracted:\n{phone_numbers}")
        print(f"[INFO] The number of phone numbers: {len(phone_numbers)}")

    links = extract_links(parsed_html)

    if not links:
        print("[INFO] No link found.")
    else:
        print(f"[INFO] The links are extracted:\n{links}")
        print(f"[INFO] The number of links: {len(links)}")

    social_media = extract_social_media(links)

    if not social_media:
        print("[INFO] No social_media_contact found.")
    else:
        print(f"[INFO] The social_media_contacts are extracted:\n{social_media}")
        print(f"[INFO] The number of social_media_contacts: {len(social_media)}")

    contacts = {"Email": emails,
                    "Phone number": phone_numbers,
                    **social_media}

    if not contacts:
        await update.message.reply_text("There is no contacts on this website ❌")
        print("[INFO] No contact found.")
        return

    await update.message.reply_text(f"Contacts are extracted ✅\
                                    \nEmails: {len(emails)}\
                                    \nPhone Numbers: {len(phone_numbers)}\
                                    \nSocial media:{len(social_media)}")

    print(f"[INFO] The contacts are extracted:\n{contacts}")
    print(f"[INFO] The number of contacts: {len(contacts)}")

    save_contacts("output/contacts.xlsx", normalized_url, contacts)
    print("[INFO] THE CONTACTS ARE SAVED.")

    with open("output/contacts.xlsx", "rb") as file:
        await update.message.reply_document(
            document=file,
            filename="contacts.xlsx",
            caption="Here is your extracted contacts Excel file! 📊"
        )

    print("[INFO] THE EXCEL FILE IS SENT.")


def main():
    """
    Initialize and run the Telegram bot.

    Loads the bot token from environment variables, creates the
    Telegram application, registers the command and message handlers,
    and starts polling for incoming updates.

    Returns
    -------
    None
        Runs the Telegram bot until it is stopped.

    Raises
    ------
    RuntimeError
        If the ``TELEGRAM_BOT_TOKEN`` environment variable is not set.
    """
    if not token:
        raise RuntimeError("[ERROR] TELEGRAM_BOT_TOKEN is not set in .env")

    application = (Application.builder()
                  .token(token)
                  .build())

    application.add_handler(CommandHandler("start", start))

    print("[INFO] Bot is starting...")

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
