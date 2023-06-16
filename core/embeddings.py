import openai


def embed_question(question: str):
    """
    Embeds the question into a vector space

    :param question: string
    :return: vectorized question
    """
    response = openai.Embedding.create(input=question, model="text-embedding-ada-002")

    return response["data"][0]["embedding"]
