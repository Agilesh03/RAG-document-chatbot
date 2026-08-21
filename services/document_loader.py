import fitz
from docx import Document
from docx.document import Document as _Document
from docx.table import Table
from docx.text.paragraph import Paragraph
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P


def extract_pdf_text(file_path):
    """
    Extract text from a PDF.
    """

    text = ""

    pdf = fitz.open(file_path)

    for page in pdf:
        page_text = page.get_text()

        if page_text:
            text += page_text + "\n"

    pdf.close()

    return text


def iter_block_items(parent):
    """
    Yield paragraphs and tables in their original
    document order.
    """

    if isinstance(parent, _Document):
        parent_element = parent.element.body
    else:
        parent_element = parent._tc

    for child in parent_element.iterchildren():

        if isinstance(child, CT_P):

            yield Paragraph(
                child,
                parent
            )

        elif isinstance(child, CT_Tbl):

            yield Table(
                child,
                parent
            )


def extract_docx_text(file_path):
    """
    Extract both paragraphs and tables from DOCX.
    """

    document = Document(file_path)

    text_parts = []

    for block in iter_block_items(document):

        # Normal paragraph
        if isinstance(block, Paragraph):

            paragraph_text = block.text.strip()

            if paragraph_text:
                text_parts.append(
                    paragraph_text
                )

        # Table
        elif isinstance(block, Table):

            for row in block.rows:

                row_values = []

                for cell in row.cells:

                    cell_text = cell.text.strip()

                    if cell_text:
                        row_values.append(
                            cell_text
                        )

                if row_values:

                    text_parts.append(
                        " | ".join(row_values)
                    )

    return "\n".join(text_parts)


def extract_text(file_path, file_extension):

    if file_extension == ".pdf":

        return extract_pdf_text(
            file_path
        )

    elif file_extension == ".docx":

        return extract_docx_text(
            file_path
        )

    else:

        raise ValueError(
            "Unsupported file type"
        )