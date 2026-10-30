from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import ContextTypes


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.massage.reply_text("Hello! Welcome to Web Contact Extractor."
    "\n\n Please send me a website URL.")


def main():
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")
    else:
        start()

    print("Waiting for user input...")


if __name__ == "__main__":
    main()
