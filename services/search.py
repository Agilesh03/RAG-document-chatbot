import os
import faiss
import pickle
import numpy as np

from services.embedding import create_embeddings


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


INDEX_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "index.faiss"
)


METADATA_PATH = os.path.join(
    BASE_DIR,
    "vector_store",
    "metadata.pkl"
)


# ============================================================
# LOAD VECTOR STORE
# ============================================================

def load_vector_store():

    if not os.path.exists(INDEX_PATH):
        return None, []

    if not os.path.exists(METADATA_PATH):
        return None, []

    index = faiss.read_index(
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "rb"
    ) as file:

        chunks = pickle.load(file)

    return index, chunks


# ============================================================
# SEARCH
# ============================================================

def search(
    query,
    top_k=3
):
    """
    Search for the most relevant chunks.
    """

    index, chunks = load_vector_store()

    if index is None:
        return []

    if not chunks:
        return []

    query_embedding = create_embeddings(
        [query]
    )

    query_embedding = np.asarray(
        query_embedding,
        dtype="float32"
    )

    actual_top_k = min(
        top_k,
        index.ntotal
    )

    distances, indices = index.search(
        query_embedding,
        actual_top_k
    )

    results = []

    for distance, index_number in zip(
        distances[0],
        indices[0]
    ):

        if index_number < 0:
            continue

        if index_number >= len(chunks):
            continue

        item = chunks[index_number]

        # New metadata format
        if isinstance(item, dict):

            results.append({
                "chunk": item.get(
                    "chunk",
                    ""
                ),

                "filename": item.get(
                    "filename",
                    "Unknown document"
                ),

                "distance": float(
                    distance
                )
            })

        # Backward compatibility
        else:

            results.append({
                "chunk": str(item),

                "filename": "Document",

                "distance": float(
                    distance
                )
            })

    return results


# ============================================================
# TEST SEARCH
# ============================================================

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
            "Document:",
            result["filename"]
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