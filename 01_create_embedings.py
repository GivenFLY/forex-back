"""Creating embeddings for FAQ questions."""
import json
import os
import time

import dotenv
import pandas as pd

dotenv.read_dotenv()

from core.question import Question


def main():
    questions = json.load(open("static/FAQ.json", "r", encoding="utf-8"))

    frames = []

    for idx, question in enumerate(questions):
        print(f"({idx + 1}/{len(questions)})\tEmbedding {question['Question_short']}")
        q = Question(**question)
        frames.append(q.dataframe)
        time.sleep(0.5)

    data_frame = pd.concat(frames, ignore_index=True)
    data_frame.to_pickle("static/FAQ.pkl")


if __name__ == "__main__":
    main()
