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

    # Check if text contains CJK characters (U+4E00–U+9FFF basic block)
    has_cjk = any("\u4e00" <= c <= "\u9fff" for c in text)
    if has_cjk:
        # Show a clear notice instead of garbled/missing glyphs
        pdf.set_font("Helvetica", "I", size=10)
        pdf.multi_cell(
            0, 7,
            "[Note: PDF export has limited Chinese character support. "
            "Please use DOCX download for Chinese text.]"
        )
        pdf.ln(3)
        pdf.set_font("Helvetica", size=11)
        # Replace CJK chars with underscores so Latin portions still render
        text = "".join(
            c if not ("\u4e00" <= c <= "\u9fff") else "_" for c in text
        )

    for para in text.split("\n\n"):
        stripped = para.strip()
        if stripped:
            pdf.multi_cell(0, 7, stripped)
            pdf.ln(3)
    return bytes(pdf.output())
