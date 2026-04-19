import { downloadFile } from "../api";
import { useState } from "react";

export default function ResultPanel({ result, isProcessing, error }) {
  const [copied, setCopied] = useState(false);

  async function handleCopy() {
    try {
      await navigator.clipboard.writeText(result);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch (err) {
      alert("复制失败，请手动选择文本复制");
    }
  }

  async function handleDownload(format) {
    try {
      await downloadFile(result, format);
    } catch (err) {
      alert(`下载失败：${err.message}`);
    }
  }

  return (
    <div className="flex flex-col gap-4 p-4 border-l border-gray-200 h-full">
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-700">处理结果</h2>
        {result && !isProcessing && (
          <div className="flex gap-2">
            <button onClick={handleCopy} className="text-xs px-2 py-1 border border-gray-300 rounded hover:bg-gray-50">
              {copied ? "✓ 已复制" : "复制"}
            </button>
            <button onClick={() => handleDownload("docx")} className="text-xs px-2 py-1 border border-blue-300 text-blue-600 rounded hover:bg-blue-50">
              下载 DOCX
            </button>
            <button onClick={() => handleDownload("pdf")} className="text-xs px-2 py-1 border border-blue-300 text-blue-600 rounded hover:bg-blue-50">
              下载 PDF
            </button>
          </div>
        )}
      </div>

      {error && (
        <div className="p-3 bg-red-50 border border-red-200 rounded text-sm text-red-600">
          {error}
        </div>
      )}

      <div className="flex-1 border border-gray-200 rounded p-3 overflow-auto">
        {result ? (
          <p className="text-sm whitespace-pre-wrap text-gray-800">
            {result}
            {isProcessing && <span className="inline-block w-1 h-4 bg-blue-500 ml-0.5 animate-pulse" />}
          </p>
        ) : (
          <p className="text-sm text-gray-400">结果将在此显示…</p>
        )}
      </div>
    </div>
  );
}
