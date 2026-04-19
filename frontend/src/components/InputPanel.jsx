import { useRef, useState } from "react";
import { parseFile } from "../api";

const MODES = [
  { value: "restyle", label: "改语气" },
  { value: "shorten", label: "缩写" },
  { value: "expand", label: "扩写" },
];

export default function InputPanel({ text, onTextChange, mode, onModeChange, instruction, onInstructionChange, onProcess, isProcessing }) {
  const fileRef = useRef();
  const [dragOver, setDragOver] = useState(false);

  async function handleFileLoad(file) {
    try {
      const extracted = await parseFile(file);
      onTextChange(extracted);
    } catch (err) {
      alert(`文件解析失败：${err.message}`);
    }
  }

  const canProcess = isProcessing || (text.trim().length > 0 && mode !== "");

  return (
    <div className="flex flex-col gap-4 p-4 h-full">
      <h2 className="text-lg font-semibold text-gray-700">论文输入</h2>

      <div
        className={`relative flex-1 border-2 rounded transition ${dragOver ? "border-blue-400 bg-blue-50" : "border-gray-300"}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={(e) => { if (!e.currentTarget.contains(e.relatedTarget)) setDragOver(false); }}
        onDrop={(e) => { e.preventDefault(); setDragOver(false); const f = e.dataTransfer.files[0]; if (f) handleFileLoad(f); }}
      >
        <textarea
          value={text}
          onChange={(e) => onTextChange(e.target.value)}
          placeholder="在此粘贴论文内容，或将文件拖拽到此区域（支持 .txt / .pdf / .docx）"
          className="w-full h-full p-3 text-sm resize-none focus:outline-none bg-transparent"
        />
        <button
          onClick={() => fileRef.current.click()}
          className="absolute bottom-3 right-3 text-xs text-gray-400 hover:text-blue-500 underline"
        >
          上传文件
        </button>
        <input ref={fileRef} type="file" accept=".txt,.pdf,.docx" className="hidden" onChange={(e) => { const f = e.target.files[0]; if (f) handleFileLoad(f); e.target.value = ""; }} />
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-2">操作模式</label>
        <div className="flex gap-3">
          {MODES.map((m) => (
            <label key={m.value} className="flex items-center gap-1 cursor-pointer text-sm">
              <input type="radio" name="mode" value={m.value} checked={mode === m.value} onChange={() => onModeChange(m.value)} className="accent-blue-500" />
              {m.label}
            </label>
          ))}
        </div>
      </div>

      {(mode === "shorten" || mode === "expand") && (
        <div>
          <label className="block text-sm font-medium text-gray-600 mb-1">
            {mode === "shorten" ? "缩写指令" : "扩写指令"}
          </label>
          <input
            value={instruction}
            onChange={(e) => onInstructionChange(e.target.value)}
            placeholder={mode === "shorten" ? "例如：压缩到3000字 / 把第二节压缩到两段" : "例如：扩展到5000字 / 把结论部分写得更有说服力"}
            className="w-full p-2 border border-gray-300 rounded text-sm focus:outline-none focus:ring-1 focus:ring-blue-400"
          />
        </div>
      )}

      <button
        onClick={onProcess}
        disabled={!canProcess}
        className={`py-2 px-4 rounded font-medium text-white transition ${
          isProcessing ? "bg-red-500 hover:bg-red-600" : canProcess ? "bg-blue-500 hover:bg-blue-600" : "bg-gray-300 cursor-not-allowed"
        }`}
      >
        {isProcessing ? "⬛ 停止" : "▶ 开始处理"}
      </button>
    </div>
  );
}
