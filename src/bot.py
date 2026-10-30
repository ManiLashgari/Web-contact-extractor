from dotenv import load_dotenv
import os


load_dotenv()
token = os.getenv("TELEGRAM_BOT_TOKEN")


def main():
    if not token:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set in .env")

    print("Waiting for user input...")


if __name__ == "__main__":
    main()
