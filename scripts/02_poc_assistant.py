"""Proof of concept for the FAQ assistant."""
import os
from pprint import pprint

import dotenv

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.read_dotenv(os.path.join(BASE_DIR, ".env"))

from core.assistant import FAQAssistant


def main():
    assistant = FAQAssistant(
        embeddings_file_path=os.path.join(BASE_DIR, "static/FAQ.pkl"),
        faq_file_path=os.path.join(BASE_DIR, "static/FAQ.json"),
    )

    while True:
        question = input("Ask me: ")
        pprint(assistant.answer(question))


if __name__ == "__main__":
    main()
