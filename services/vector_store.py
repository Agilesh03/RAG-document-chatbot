import faiss
import numpy as np
import pickle
import os


# ============================================================
# BASE PATH
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


VECTOR_STORE_DIR = os.path.join(
    BASE_DIR,
    "vector_store"
)


INDEX_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "index.faiss"
)


METADATA_PATH = os.path.join(
    VECTOR_STORE_DIR,
    "metadata.pkl"
)


# ============================================================
# CREATE VECTOR INDEX
# ============================================================

def create_vector_index(embeddings):
    """
    Create a FAISS index from embedding vectors.
    """

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    if embeddings.size == 0:
        raise ValueError(
            "No embeddings were provided."
        )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        embeddings
    )

    return index


# ============================================================
# SAVE VECTOR STORE
# ============================================================

def save_vector_store(
    index,
    chunks
):
    """
    Save FAISS index and metadata.
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


# ============================================================
# LOAD VECTOR STORE
# ============================================================

def load_vector_store():
    """
    Load FAISS index and metadata.
    """

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