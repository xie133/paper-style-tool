MAX_SAMPLE_CHARS = 24000  # ~8000 tokens combined

def detect_language(text: str) -> str:
    chinese_chars = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    return "zh" if chinese_chars / max(len(text), 1) > 0.3 else "en"

def build_messages(
    text: str,
    mode: str,
    style_samples: list[str],
    style_description: str,
    instruction: str,
) -> dict:
    lang = detect_language(text)
    combined_samples = "\n\n---\n\n".join(style_samples)
    if len(combined_samples) > MAX_SAMPLE_CHARS:
        combined_samples = combined_samples[:MAX_SAMPLE_CHARS] + "\n[样本已截断]"

    if lang == "zh":
        system = _build_system_zh(mode, combined_samples, style_description, instruction)
        user = f"请处理以下论文：\n\n{text}"
    else:
        system = _build_system_en(mode, combined_samples, style_description, instruction)
        user = f"Please process the following paper:\n\n{text}"

    return {"system": system, "user": user}

def _build_system_zh(mode, samples, description, instruction):
    base = "你是一个学术写作助手。"
    style_block = ""
    if samples:
        style_block += f"\n\n【用户写作风格样本】\n{samples}"
    if description:
        style_block += f"\n\n【风格描述】\n{description}"

    if mode == "restyle":
        task = "请严格按照上述风格改写用户提供的论文。论文的内容、论点、数据和结构不得改变，只调整语气和表达方式。"
    elif mode == "shorten":
        task = f"请按照上述风格改写论文，同时压缩篇幅。要求：{instruction}"
    else:  # expand
        task = f"请按照上述风格改写论文，同时扩展篇幅。要求：{instruction}"

    return base + style_block + f"\n\n【任务】\n{task}"

def _build_system_en(mode, samples, description, instruction):
    base = "You are an academic writing assistant."
    style_block = ""
    if samples:
        style_block += f"\n\n[User's writing style samples]\n{samples}"
    if description:
        style_block += f"\n\n[Style description]\n{description}"

    if mode == "restyle":
        task = "Rewrite the user's paper in the style above. Do NOT change the content, arguments, data, or structure — only adjust tone and phrasing."
    elif mode == "shorten":
        task = f"Rewrite the paper in the style above while reducing its length. Requirement: {instruction}"
    else:  # expand
        task = f"Rewrite the paper in the style above while expanding its length. Requirement: {instruction}"

    return base + style_block + f"\n\n[Task]\n{task}"
