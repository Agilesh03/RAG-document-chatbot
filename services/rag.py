from search import search
from llm import generate_answer


def ask_question(question):
    """
    Retrieve relevant chunks and generate
    an answer using the LLM.
    """

    results = search(
        question,
        top_k=3
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


if __name__ == "__main__":

    question = input(
        "\nAsk a question about the document: "
    )

    answer = ask_question(
        question
    )

    print(
        "\n========== ANSWER ==========\n"
    )

    print(answer)
