import faiss
import pickle
import numpy as np

from embedding import create_embeddings


INDEX_PATH = "../vector_store/index.faiss"
METADATA_PATH = "../vector_store/metadata.pkl"


def load_vector_store():
    """
    Load the saved FAISS index and document chunks.
    """

    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "rb"
    ) as file:

        chunks = pickle.load(file)

    return index, chunks


def search(query, top_k=3):
    """
    Search the vector store for the
    most relevant document chunks.
    """

    index, chunks = load_vector_store()

    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

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