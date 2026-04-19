import os
import anthropic

MAX_TEXT_CHARS = 180000  # ~60k tokens

_api_key = os.environ.get("ANTHROPIC_API_KEY")
if not _api_key:
    raise RuntimeError(
        "ANTHROPIC_API_KEY environment variable is not set. "
        "Please edit .env file in the project root and set your API key."
    )

client = anthropic.Anthropic(api_key=_api_key)

def stream_completion(system: str, user: str):
    """Yields text chunks from Claude streaming response using raw SSE event iteration."""
    if len(user) > MAX_TEXT_CHARS:
        raise ValueError(
            "Paper text exceeds maximum length (~45,000 Chinese characters). "
            "Please shorten it."
        )

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=8096,
        system=system,
        messages=[{"role": "user", "content": user}],
        stream=True,
    )
    for event in response:
        if hasattr(event, "type") and event.type == "content_block_delta":
            if hasattr(event, "delta") and hasattr(event.delta, "text"):
                yield event.delta.text
