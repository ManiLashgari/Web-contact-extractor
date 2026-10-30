from dotenv import load_dotenv
import os
from telegram import Update
from telegram.ext import (ContextTypes,
                          Application,
                          CommandHandler,
                          MessageHandler,
                          filters)


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Welcome to Web Contact Extractor."
    "\n\n Please send me a website URL.")


async def handle_message(update: Update, context: ContextTypes):
    message = update.message.text
    print(f"Recived message: {message}")
    await update.message.reply_text(f"You sent: {message}")


def main():
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")

    application = (Application.builder()
                  .token(token)
                  .build())

    application.add_handler(CommandHandler("start", start))

    print("Bot is starting...")

    application.add_handler(MessageHandler(
        filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()
