from services.search import search
from services.llm import generate_answer


def ask_question(question):
    """
    Retrieve relevant document chunks
    and generate an answer using Llama.
    """

    results = search(
        question,
        top_k=3
    )


    if not results:

        return (
            "I could not find any processed "
            "documents to answer this question."
        )


    context_parts = []


    for result in results:

        context_parts.append(
            result["chunk"]
        )


    context = "\n\n".join(
        context_parts
    )


    answer = generate_answer(
        question,
        context
    )


    return answer