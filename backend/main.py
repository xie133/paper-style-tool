import os
import tempfile
import json
from fastapi import FastAPI, UploadFile, File, HTTPException, Response
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from file_parser import extract_text
from prompt_builder import build_messages
from claude_client import stream_completion
from downloader import generate_docx_bytes, generate_pdf_bytes

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}


ALLOWED_TYPES = {
    "text/plain",
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/msword",
}
MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB

@app.post("/api/parse")
async def parse_file(file: UploadFile = File(...)):
    if file.content_type not in ALLOWED_TYPES:
        raise HTTPException(400, f"Unsupported file type: {file.content_type}")
    data = await file.read()
    if len(data) > MAX_FILE_BYTES:
        raise HTTPException(413, "File exceeds 10 MB limit")
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        tmp.write(data)
        tmp_path = tmp.name
    try:
        text = extract_text(tmp_path, file.content_type)
    except ValueError as e:
        raise HTTPException(400, str(e))
    finally:
        os.unlink(tmp_path)
    return {"text": text}


class ProcessRequest(BaseModel):
    text: str
    mode: str  # "restyle" | "shorten" | "expand"
    style_samples: list[str] = []
    style_description: str = ""
    instruction: str = ""

@app.post("/api/process")
async def process_paper(req: ProcessRequest):
    if req.mode not in ("restyle", "shorten", "expand"):
        raise HTTPException(400, "mode must be restyle, shorten, or expand")
    if not req.text.strip():
        raise HTTPException(400, "text is required")

    try:
        msgs = build_messages(
            text=req.text,
            mode=req.mode,
            style_samples=req.style_samples,
            style_description=req.style_description,
            instruction=req.instruction,
        )
    except Exception as e:
        raise HTTPException(400, str(e))

    def event_stream():
        try:
            for chunk in stream_completion(msgs["system"], msgs["user"]):
                yield f"data: {json.dumps({'text': chunk})}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
        except Exception as e:
            yield f"data: {json.dumps({'error': 'Claude API error: ' + str(e)})}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


class DownloadRequest(BaseModel):
    text: str
    format: str  # "docx" | "pdf"

@app.post("/api/download")
def download_file(req: DownloadRequest):
    MAX_DOWNLOAD_CHARS = 500_000
    if len(req.text) > MAX_DOWNLOAD_CHARS:
        raise HTTPException(400, "text too large for download")
    if req.format == "docx":
        data = generate_docx_bytes(req.text)
        return Response(
            content=data,
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": "attachment; filename=result.docx"},
        )
    elif req.format == "pdf":
        data = generate_pdf_bytes(req.text)
        return Response(
            content=data,
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=result.pdf"},
        )
    else:
        raise HTTPException(400, "format must be docx or pdf")
