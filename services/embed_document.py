from document_loader import extract_text
from chunker import create_chunks
from embedding import create_embeddings
from vector_store import create_vector_index, save_vector_store


DOCUMENT_PATH = "../documents/MS_Dhoni_History_and_Career.docx"


# Step 1: Extract text
text = extract_text(
    DOCUMENT_PATH,
    ".docx"
)

print("Text extracted successfully.")
print("Total characters:", len(text))


# Step 2: Create chunks
chunks = create_chunks(text)

print("\nTotal chunks:", len(chunks))


# Step 3: Create embeddings
embeddings = create_embeddings(chunks)

print("\nEmbeddings created successfully.")
print("Embedding shape:", embeddings.shape)

index = create_vector_index(
    embeddings
)

save_vector_store(
    index,
    chunks
)


# Step 4: Display information about each chunk
print("\n========== CHUNK + EMBEDDING INFO ==========\n")

for index, chunk in enumerate(chunks):

    print(f"Chunk {index + 1}")
    print("----------------------------------------")
    print(chunk[:200])

    print(
        "Embedding dimensions:",
        len(embeddings[index])
    )

    print()