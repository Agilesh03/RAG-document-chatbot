import ollama


MODEL_NAME = "llama3.2"


def generate_answer(question, context):
    """
    Generate an answer using only the retrieved context.
    """

    prompt = f"""
You are an AI document assistant.

Answer the user's question using ONLY the
information provided in the context below.

If the answer is not present in the context,
say:

"I could not find the answer in the document."

Do not use outside knowledge.

Context:
{context}

Question:
{question}

Answer:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response[
        "message"
    ][
        "content"
    ]