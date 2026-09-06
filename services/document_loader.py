from pypdf import PdfReader
from docx import Document


# ============================================================
# PDF
# ============================================================

def extract_pdf_text(file_path):
    """
    Extract text from a PDF document.
    """

    reader = PdfReader(
        file_path
    )

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:

            pages.append(
                text
            )

    return "\n".join(
        pages
    )


# ============================================================
# DOCX
# ============================================================

def extract_docx_text(file_path):
    """
    Extract text from a DOCX document.
    """

    document = Document(
        file_path
    )

    paragraphs = []

    for paragraph in document.paragraphs:

        text = paragraph.text.strip()

        if text:

            paragraphs.append(
                text
            )

    return "\n".join(
        paragraphs
    )


# ============================================================
# GENERAL EXTRACTOR
# ============================================================

def extract_text(file_path, extension):
    """
    Extract text based on file extension.
    """

    extension = extension.lower()

    if extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    elif extension == ".docx":

        return extract_docx_text(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported document format."
        )