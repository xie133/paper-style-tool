from prompt_builder import build_messages, detect_language

def test_detect_chinese():
    assert detect_language("这是一篇中文论文，内容关于深度学习。") == "zh"

def test_detect_english():
    assert detect_language("This is an English paper about deep learning.") == "en"

def test_restyle_includes_sample():
    msgs = build_messages(
        text="My paper content.",
        mode="restyle",
        style_samples=["Sample writing I did."],
        style_description="concise, active voice",
        instruction="",
    )
    system = msgs["system"]
    assert "Sample writing I did." in system
    assert "concise, active voice" in system
    assert "content" in system.lower()

def test_shorten_includes_instruction():
    msgs = build_messages(
        text="Long paper.",
        mode="shorten",
        style_samples=[],
        style_description="",
        instruction="reduce to 500 words",
    )
    assert "500 words" in msgs["system"] or "500 words" in msgs["user"]

def test_expand_mode():
    msgs = build_messages(
        text="Short paper.",
        mode="expand",
        style_samples=[],
        style_description="",
        instruction="expand to 2000 words",
    )
    assert "expand" in msgs["system"].lower() or "expand" in msgs["user"].lower()
