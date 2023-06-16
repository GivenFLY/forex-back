"""Proof of concept for the FAQ assistant."""
import os
from pprint import pprint

import dotenv

dotenv.read_dotenv()

from core.assistant import FAQAssistant


def main():
    assistant = FAQAssistant(
        embeddings_file_path="static/FAQ.pkl",
        faq_file_path="static/static/FAQ.json",
    )

    while True:
        question = input("Ask me: ")
        pprint(assistant.answer(question))


if __name__ == "__main__":
    main()
