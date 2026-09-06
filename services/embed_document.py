import os

from services.document_loader import extract_text
from services.chunker import create_chunks
from services.embedding import create_embeddings
from services.vector_store import (
    create_vector_index,
    save_vector_store
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DOCUMENTS_DIR = os.path.join(
    BASE_DIR,
    "documents"
)


# ============================================================
# REBUILD VECTOR STORE
# ============================================================

def rebuild_vector_store():

    print(
        "\n========================================"
    )

    print(
        "REBUILDING VECTOR STORE"
    )

    print(
        "========================================"
    )


    os.makedirs(
        DOCUMENTS_DIR,
        exist_ok=True
    )


    all_chunks = []


    # --------------------------------------------------------
    # Find documents
    # --------------------------------------------------------

    files = []

    for filename in os.listdir(
        DOCUMENTS_DIR
    ):

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension in {
            ".pdf",
            ".docx"
        }:

            files.append(
                filename
            )


    if not files:

        print(
            "No documents found."
        )

        return 0


    # --------------------------------------------------------
    # Process every document
    # --------------------------------------------------------

    for filename in files:

        file_path = os.path.join(
            DOCUMENTS_DIR,
            filename
        )

        extension = os.path.splitext(
            filename
        )[1].lower()


        print(
            f"\nProcessing: {filename}"
        )


        # Extract
        text = extract_text(
            file_path,
            extension
        )


        if not text.strip():

            print(
                "No text found. Skipping."
            )

            continue


        # Chunk
        chunks = create_chunks(
            text
        )


        print(
            f"Chunks created: {len(chunks)}"
        )


        # Add filename to metadata
        for chunk in chunks:

            all_chunks.append({
                "filename": filename,
                "chunk": chunk
            })


    # --------------------------------------------------------
    # Check chunks
    # --------------------------------------------------------

    if not all_chunks:

        print(
            "No chunks available."
        )

        return 0


    # --------------------------------------------------------
    # Create embeddings
    # --------------------------------------------------------

    print(
        "\nCreating embeddings..."
    )


    texts = [
        item["chunk"]
        for item in all_chunks
    ]


    embeddings = create_embeddings(
        texts
    )


    print(
        "Embedding dimensions:",
        embeddings.shape[1]
    )


    # --------------------------------------------------------
    # Create FAISS
    # --------------------------------------------------------

    index = create_vector_index(
        embeddings
    )


    # --------------------------------------------------------
    # Save
    # --------------------------------------------------------

    save_vector_store(
        index,
        all_chunks
    )


    print(
        "\n========================================"
    )

    print(
        "VECTOR STORE READY"
    )

    print(
        f"Documents: {len(files)}"
    )

    print(
        f"Chunks: {len(all_chunks)}"
    )

    print(
        "========================================"
    )


    return len(all_chunks)


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    rebuild_vector_store()