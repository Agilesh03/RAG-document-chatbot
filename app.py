from flask import (
    Flask,
    render_template,
    request,
    jsonify
)

from werkzeug.utils import secure_filename

from services.rag import ask_question
from services.embed_document import rebuild_vector_store

import os


# ============================================================
# APP
# ============================================================

app = Flask(
    __name__
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)


UPLOAD_FOLDER = os.path.join(
    BASE_DIR,
    "documents"
)


app.config[
    "UPLOAD_FOLDER"
] = UPLOAD_FOLDER


ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx"
}


# ============================================================
# HOME
# ============================================================

@app.route(
    "/",
    methods=["GET"]
)
def home():

    os.makedirs(
        UPLOAD_FOLDER,
        exist_ok=True
    )


    documents = []


    for filename in os.listdir(
        UPLOAD_FOLDER
    ):

        extension = os.path.splitext(
            filename
        )[1].lower()

        if extension in ALLOWED_EXTENSIONS:

            documents.append(
                filename
            )


    documents.sort()


    return render_template(
        "index.html",
        documents=documents
    )


# ============================================================
# UPLOAD
# ============================================================

@app.route(
    "/upload",
    methods=["POST"]
)
def upload_document():

    try:

        if "document" not in request.files:

            return jsonify({
                "success": False,
                "error": "No document selected."
            }), 400


        file = request.files[
            "document"
        ]


        if not file.filename:

            return jsonify({
                "success": False,
                "error": "No document selected."
            }), 400


        filename = secure_filename(
            file.filename
        )


        extension = os.path.splitext(
            filename
        )[1].lower()


        if extension not in ALLOWED_EXTENSIONS:

            return jsonify({
                "success": False,
                "error":
                    "Only PDF and DOCX files are supported."
            }), 400


        os.makedirs(
            UPLOAD_FOLDER,
            exist_ok=True
        )


        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        # Save document
        file.save(
            file_path
        )


        print(
            f"\nUploaded: {filename}"
        )


        # ----------------------------------------------------
        # REBUILD VECTOR STORE
        # ----------------------------------------------------

        chunks_count = rebuild_vector_store()


        return jsonify({

            "success": True,

            "filename": filename,

            "chunks": chunks_count,

            "message":
                "Document uploaded and processed successfully."
        })


    except Exception as e:

        print(
            "UPLOAD ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# ASK AI
# ============================================================

@app.route(
    "/ask",
    methods=["POST"]
)
def ask():

    try:

        data = request.get_json(
            silent=True
        )


        if not data:

            return jsonify({
                "success": False,
                "error":
                    "No request data received."
            }), 400


        question = data.get(
            "question",
            ""
        ).strip()


        if not question:

            return jsonify({
                "success": False,
                "error":
                    "Please enter a question."
            }), 400


        answer = ask_question(
            question
        )


        return jsonify({

            "success": True,

            "answer": answer

        })


    except Exception as e:

        print(
            "ASK ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# REMOVE DOCUMENT
# ============================================================

@app.route(
    "/remove/<filename>",
    methods=["DELETE"]
)
def remove_document(filename):

    try:

        filename = secure_filename(
            filename
        )


        file_path = os.path.join(
            UPLOAD_FOLDER,
            filename
        )


        if not os.path.exists(
            file_path
        ):

            return jsonify({

                "success": False,

                "error":
                    "Document not found."

            }), 404


        # Remove physical document
        os.remove(
            file_path
        )


        print(
            f"\nRemoved: {filename}"
        )


        # Rebuild vector store
        chunks_count = rebuild_vector_store()


        return jsonify({

            "success": True,

            "message":
                "Document removed successfully.",

            "chunks": chunks_count

        })


    except Exception as e:

        print(
            "REMOVE ERROR:",
            e
        )


        return jsonify({

            "success": False,

            "error": str(e)

        }), 500


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    app.run(
        debug=True
    )