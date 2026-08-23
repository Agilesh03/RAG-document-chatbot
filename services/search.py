import numpy as np

from services.embedding import create_embeddings
from services.vector_store import load_vector_store


def search(query, top_k=3):
    """
    Search the vector store for the
    most relevant document chunks.
    """

    index, chunks = load_vector_store()

    # Convert the user's question into an embedding
    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):

        if index_number == -1:
            continue

        results.append({
            "chunk": chunks[index_number],
            "distance": float(distance)
        })

    return results


if __name__ == "__main__":

    query = input(
        "\nAsk a question about the document: "
    )

    results = search(
        query,
        top_k=3
    )

    print(
        "\n========== SEARCH RESULTS ==========\n"
    )

    for number, result in enumerate(
        results,
        start=1
    ):

        print(
            f"Result {number}"
        )

        print(
            "Distance:",
            result["distance"]
        )

        print(
            "Chunk:"
        )

        print(
            result["chunk"]
        )

        print(
            "\n-----------------------------------\n"
        )