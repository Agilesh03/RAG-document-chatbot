from sentence_transformers import SentenceTransformer


# ============================================================
# EMBEDDING MODEL
# ============================================================

MODEL_NAME = (
    "sentence-transformers/all-MiniLM-L6-v2"
)


model = SentenceTransformer(
    MODEL_NAME
)


# ============================================================
# CREATE EMBEDDINGS
# ============================================================

def create_embeddings(chunks):
    """
    Convert text chunks into numerical vectors.
    """

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings