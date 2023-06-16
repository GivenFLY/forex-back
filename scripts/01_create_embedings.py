"""Creating embeddings for FAQ questions."""

import json
import os
import time

import dotenv
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dotenv.read_dotenv(os.path.join(BASE_DIR, ".env"))

from core.question import Question


def main():
    questions = json.load(
        open(os.path.join(BASE_DIR, "static/FAQ.json"), "r", encoding="utf-8")
    )

    frames = []

    for idx, question in enumerate(questions):
        print(f"({idx + 1}/{len(questions)})\tEmbedding {question['Question_short']}")
        q = Question(**question)
        frames.append(q.dataframe)
        time.sleep(0.5)

    data_frame = pd.concat(frames, ignore_index=True)
    data_frame.to_pickle(os.path.join(BASE_DIR, "static/FAQ.pkl"))


if __name__ == "__main__":
    main()
