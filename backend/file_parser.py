import pdfplumber
from docx import Document


def extract_text(filepath: str, content_type: str) -> str:
    if content_type == "text/plain":
        with open(filepath, encoding="utf-8") as f:
            return f.read()
    elif content_type == "application/pdf":
        with pdfplumber.open(filepath) as pdf:
            return "\n".join(
                page.extract_text() or "" for page in pdf.pages
            ).strip()
    elif content_type in (
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/msword",
    ):
        doc = Document(filepath)
        return "\n".join(p.text for p in doc.paragraphs).strip()
    else:
        raise ValueError(f"Unsupported file type: {content_type}")
