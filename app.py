from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename

from services.document_loader import extract_text
from services.chunker import create_chunks
from services.embedding import create_embeddings
from services.vector_store import (
    create_vector_index,
    save_vector_store
)
from services.rag import ask_question

import os


app = Flask(__name__)


# =========================================================
# Configuration
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "documents"
)

VECTOR_STORE_FOLDER = os.path.join(
    BASE_DIR,
    "vector_store"
)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# Make sure required folders exist
os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)

os.makedirs(
    VECTOR_STORE_FOLDER,
    exist_ok=True
)


# =========================================================
# Home Page
# =========================================================

@app.route("/")
def home():

    return render_template(
        "index.html"
    )


# =========================================================
# Upload Document
# =========================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_document():

    try:

        # ---------------------------------------------
        # Check file
        # ---------------------------------------------

        if "document" not in request.files:

            return render_template(
                "index.html",
                error="No document selected."
            )


        file = request.files["document"]


        if file.filename == "":

            return render_template(
                "index.html",
                error="No document selected."
            )


        # ---------------------------------------------
        # Secure filename
        # ---------------------------------------------

        filename = secure_filename(
            file.filename
        )


        extension = os.path.splitext(
            filename
        )[1].lower()


        # ---------------------------------------------
        # Validate extension
        # ---------------------------------------------

        if extension not in ALLOWED_EXTENSIONS:

            return render_template(
                "index.html",
                error=(
                    "Only PDF and DOCX files "
                    "are supported."
                )
            )


        # ---------------------------------------------
        # Save file
        # ---------------------------------------------

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(
            file_path
        )


        # ---------------------------------------------
        # Extract text
        # ---------------------------------------------

        extracted_text = extract_text(
            file_path,
            extension
        )


        # ---------------------------------------------
        # Create chunks
        # ---------------------------------------------

        chunks = create_chunks(
            extracted_text
        )


        if not chunks:

            return render_template(
                "index.html",
                error=(
                    "No readable content was "
                    "found in the document."
                )
            )


        # ---------------------------------------------
        # Create embeddings
        # ---------------------------------------------

        embeddings = create_embeddings(
            chunks
        )


        # ---------------------------------------------
        # Create FAISS index
        # ---------------------------------------------

        index = create_vector_index(
            embeddings
        )


        # ---------------------------------------------
        # Save vector store
        # ---------------------------------------------

        save_vector_store(
            index,
            chunks
        )


        # ---------------------------------------------
        # Show document information
        # ---------------------------------------------

        return render_template(
            "index.html",

            success=(
                "Document uploaded and processed "
                "successfully."
            ),

            filename=filename,

            text=extracted_text,

            chunks=chunks
        )


    except Exception as e:

        print(
            "Upload Error:",
            str(e)
        )

        return render_template(
            "index.html",
            error=str(e)
        )


# =========================================================
# Ask Question
# =========================================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    try:

        # ---------------------------------------------
        # Get question
        # ---------------------------------------------

        question = request.form.get(
            "question",
            ""
        ).strip()


        # ---------------------------------------------
        # Validate question
        # ---------------------------------------------

        if not question:

            return render_template(
                "index.html",
                error="Please enter a question."
            )


        # ---------------------------------------------
        # RAG
        # ---------------------------------------------

        answer = ask_question(
            question
        )


        # ---------------------------------------------
        # Show answer
        # ---------------------------------------------

        return render_template(
            "index.html",

            question=question,

            answer=answer
        )


    except FileNotFoundError:

        return render_template(
            "index.html",
            error=(
                "Please upload and process a "
                "document before asking a question."
            )
        )


    except Exception as e:

        print(
            "Question Error:",
            str(e)
        )

        return render_template(
            "index.html",
            error=str(e)
        )


# =========================================================
# Run Application
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )