from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def create_embeddings(chunks):
    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings


if __name__ == "__main__":

    test_chunks = [
        "Dhoni scored an unbeaten 183 against Sri Lanka.",
        "Dhoni captained India in the 2007 T20 World Cup.",
        "Chennai Super Kings won IPL titles under Dhoni's leadership."
    ]

    embeddings = create_embeddings(test_chunks)

    print("Number of chunks:", len(embeddings))

    print("Embedding dimensions:", embeddings.shape)

    print("\nFirst embedding:")

    print(embeddings[0])