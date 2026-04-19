const BASE = "http://localhost:8000";

export async function parseFile(file) {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${BASE}/api/parse`, { method: "POST", body: form });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || "Parse failed");
  }
  return (await res.json()).text;
}

export function streamProcess({ text, mode, styleSamples, styleDescription, instruction }, onChunk, onError, onDone) {
  const controller = new AbortController();

  fetch(`${BASE}/api/process`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      text,
      mode,
      style_samples: styleSamples,
      style_description: styleDescription,
      instruction,
    }),
    signal: controller.signal,
  }).then(async (res) => {
    if (!res.ok) {
      const err = await res.json();
      onError(err.detail || "Process failed");
      return;
    }
    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop();
      for (const line of lines) {
        if (!line.startsWith("data: ")) continue;
        const payload = line.slice(6);
        if (payload === "[DONE]") { onDone(); return; }
        try {
          const parsed = JSON.parse(payload);
          if (parsed.error) { onError(parsed.error); return; }
          if (parsed.text) onChunk(parsed.text);
        } catch (e) {
          console.warn("SSE parse error:", line, e);
        }
      }
    }
    onDone();
  }).catch((e) => {
    if (e.name !== "AbortError") onError(e.message);
  });

  return () => controller.abort();
}

export async function downloadFile(text, format) {
  const res = await fetch(`${BASE}/api/download`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, format }),
  });
  if (!res.ok) throw new Error("Download failed");
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `result.${format}`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
