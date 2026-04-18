import pytest
from file_parser import extract_text

def test_extract_txt(tmp_path):
    f = tmp_path / "sample.txt"
    f.write_text("Hello world", encoding="utf-8")
    assert extract_text(str(f), "text/plain") == "Hello world"

def test_extract_unsupported_type():
    with pytest.raises(ValueError, match="Unsupported"):
        extract_text("fake.xyz", "application/octet-stream")

def test_extract_empty_txt(tmp_path):
    f = tmp_path / "empty.txt"
    f.write_text("", encoding="utf-8")
    assert extract_text(str(f), "text/plain") == ""
