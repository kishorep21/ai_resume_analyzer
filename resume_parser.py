from pypdf import PdfReader
from docx import Document


def extract_pdf_text(file):
    """Extract text from a PDF resume."""
    try:
        reader = PdfReader(file)
        text = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text)

        return "\n".join(text).strip()

    except Exception as e:
        raise ValueError(f"Unable to read PDF: {e}")


def extract_docx_text(file):
    """Extract text from a DOCX resume."""
    try:
        document = Document(file)

        paragraphs = [
            paragraph.text
            for paragraph in document.paragraphs
            if paragraph.text.strip()
        ]

        return "\n".join(paragraphs).strip()

    except Exception as e:
        raise ValueError(f"Unable to read DOCX: {e}")


def extract_resume_text(file):
    """Extract resume text based on file extension."""

    file_name = file.name.lower()

    if file_name.endswith(".pdf"):
        return extract_pdf_text(file)

    if file_name.endswith(".docx"):
        return extract_docx_text(file)

    raise ValueError("Only PDF and DOCX files are supported.")