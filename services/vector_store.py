import faiss
import numpy as np
import pickle
import os


VECTOR_STORE_DIR = "../vector_store"

INDEX_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "index.faiss"
)

METADATA_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "metadata.pkl"
)


def create_vector_index(embeddings):
    """
    Create a FAISS index from embedding vectors.
    """

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(embeddings)

    return index


def save_vector_store(index, chunks):
    """
    Save FAISS index and document chunks.
    """

    os.makedirs(
        VECTOR_STORE_DIR,
        exist_ok=True
    )

    faiss.write_index(
        index,
        INDEX_PATH
    )

    with open(
        METADATA_PATH,
        "wb"
    ) as file:

        pickle.dump(
            chunks,
            file
        )

    print("Vector store saved successfully.")

    print(
        "Index:",
        INDEX_PATH
    )

    print(
        "Metadata:",
        METADATA_PATH
    )