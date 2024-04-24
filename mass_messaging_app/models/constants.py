import os

from dotenv import load_dotenv

load_dotenv()

SCOPES: list[str] = [
    os.getenv("GOOGLE_SHEETS_API_SCOPE"),
    os.getenv("GOOGLE_GMAIL_API_SCOPE"),
]
