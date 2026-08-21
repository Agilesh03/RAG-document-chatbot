from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from services.document_loader import extract_text
from services.chunker import create_chunks
import os


app = Flask(__name__)

UPLOAD_FOLDER = "documents"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {".pdf", ".docx"}


@app.route("/", methods=["GET", "POST"])
def home():

    extracted_text = None
    chunks = []
    error = None

    if request.method == "POST":

        if "document" not in request.files:
            error = "No document selected"
            return render_template(
                "index.html",
                text=extracted_text,
                error=error
            )

        file = request.files["document"]

        if file.filename == "":
            error = "No document selected"
            return render_template(
                "index.html",
                text=extracted_text,
                error=error
            )

        filename = secure_filename(file.filename)

        extension = os.path.splitext(filename)[1].lower()

        if extension not in ALLOWED_EXTENSIONS:
            error = "Only PDF and DOCX files are supported"

            return render_template(
                "index.html",
                text=extracted_text,
                error=error
            )

        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )

        file.save(file_path)

        extracted_text = extract_text(
            file_path,
            extension
        )

        chunks = create_chunks(extracted_text)

    return render_template(
        "index.html",
        text=extracted_text,
        chunks=chunks if extracted_text else [],
        error=error
    )




if __name__ == "__main__":
    app.run(debug=True)

