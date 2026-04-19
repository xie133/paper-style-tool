from downloader import generate_docx_bytes, generate_pdf_bytes

def test_generate_docx_returns_bytes():
    result = generate_docx_bytes("Hello, this is a test paper.")
    assert isinstance(result, bytes)
    assert len(result) > 0
    # DOCX files start with PK (zip header)
    assert result[:2] == b"PK"

def test_generate_pdf_returns_bytes():
    result = generate_pdf_bytes("Hello, this is a test paper.")
    assert isinstance(result, bytes)
    assert result[:4] == b"%PDF"

def test_generate_docx_multiline():
    text = "First paragraph.\n\nSecond paragraph."
    result = generate_docx_bytes(text)
    assert isinstance(result, bytes)
    assert len(result) > 0
