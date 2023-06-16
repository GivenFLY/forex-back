import json
from functools import lru_cache
from typing import List, Tuple
import pandas as pd
from langchain.schema import BaseRetriever, Document
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

from core.embeddings import embed_question
from core.question import Question


class QuestionRetreiver(BaseRetriever):
    def __init__(
        self,
        embeddings_file_path: str,
        faq_file_path: str,
        k: int = 20,
        max_unique_questions: int = 5,
    ):
        """
        Custom retriever for FAQ

        :param embeddings_file_path: path for the embeddings file
        :param faq_file_path: path for the faq file
        :param k: parameter for the retriever
        :param max_unique_questions: maximum number of unique questions to return in relevant documents
        """
        self._embeddings = pd.read_pickle(embeddings_file_path)
        self.numeric_embeddings = self._embeddings["embeddings"].tolist()
        self._faqs = json.load(open(faq_file_path, "r", encoding="utf-8"))
        self.k = k
        self.max_unique_questions = max_unique_questions

    @property
    def faqs(self):
        return {faq["Question ID"]: Question(**faq) for faq in self._faqs}

    def as_retriever(self, k: int) -> "QuestionRetreiver":
        self.k = k
        return self

    def retrieve(self, query: str) -> List[Tuple[str, float]]:
        """:returns: a list of tuples (question_id, similarity)"""
        # Embed the query
        new_embedding = embed_question(query)

        # Compute cosine similarities
        similarities = cosine_similarity([new_embedding], self.numeric_embeddings)

        # Get the indices of the k most similar questions
        most_similar_indices = np.argsort(similarities[0])[-self.k :]

        # Return the most similar questions and their similarities
        return [
            (self._embeddings["id"][i], similarities[0][i])
            for i in most_similar_indices
        ]

    def get_relevant_documents(self, query: str) -> List[Document]:
        query_result = self.retrieve(query)
        question_id_set = list(
            set([question_id for question_id, score in query_result])
        )[: self.max_unique_questions]
        questions = [self.faqs[question_id] for question_id in question_id_set]
        return [
            Document(page_content=question.short_context_information)
            for question in questions
        ]

    async def aget_relevant_documents(self, query: str) -> List[Document]:
        return self.get_relevant_documents(query)
