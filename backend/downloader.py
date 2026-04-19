import io
from docx import Document
from fpdf import FPDF

def generate_docx_bytes(text: str) -> bytes:
    doc = Document()
    for para in text.split("\n\n"):
        stripped = para.strip()
        if stripped:
            doc.add_paragraph(stripped)
    buf = io.BytesIO()
    doc.save(buf)
    return buf.getvalue()

def generate_pdf_bytes(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Helvetica", size=11)
    for para in text.split("\n\n"):
        stripped = para.strip()
        if stripped:
            pdf.multi_cell(0, 7, stripped)
            pdf.ln(3)
    return bytes(pdf.output())
