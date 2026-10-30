from dotenv import load_dotenv
import os
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


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to Web Contact Extractor."
    "\n\nPlease send me a website URL.")


async def handle_message(update: Update, context: ContextTypes):
    message = update.message.text
    print(f"[INFO] Recived message: {message}")

    normalized_url = normalize_url(message)
    print(f"[INFO] Normalized URL: {normalized_url}")

    is_valid = is_valid_url(normalized_url)

    if not is_valid:
        await update.message.reply_text("Invalid URL ❌ Please send a valid website URL.")
        print(f"[ERROR] The URL is invalid!: {normalized_url}")
        return

    await update.message.reply_text(f"I received your URL ✅")
    print(f"[INFO] Valid URL received: {normalized_url}")


def main():
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
