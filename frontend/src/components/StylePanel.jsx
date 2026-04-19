import { useRef } from "react";
import { parseFile } from "../api";

export default function StylePanel({ samples, onSamplesChange, description, onDescriptionChange }) {
  const fileRef = useRef();

  async function handleSampleUpload(e) {
    const file = e.target.files[0];
    if (!file) return;
    try {
      const text = await parseFile(file);
      onSamplesChange([...samples, { id: crypto.randomUUID(), name: file.name, text }]);
    } catch (err) {
      alert(`样本解析失败：${err.message}`);
    }
    e.target.value = "";
  }

  return (
    <div className="flex flex-col gap-4 p-4 border-r border-gray-200 h-full">
      <h2 className="text-lg font-semibold text-gray-700">风格配置</h2>

      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">上传风格样本</label>
        <button
          onClick={() => fileRef.current.click()}
          className="w-full py-2 px-3 border-2 border-dashed border-gray-300 rounded text-sm text-gray-500 hover:border-blue-400 hover:text-blue-500 transition"
        >
          点击上传文章样本
        </button>
        <input ref={fileRef} type="file" accept=".txt,.pdf,.docx" className="hidden" onChange={handleSampleUpload} />
        {samples.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-2">
            {samples.map((s) => (
              <span key={s.id} className="flex items-center gap-1 bg-blue-100 text-blue-700 text-xs px-2 py-1 rounded-full">
                {s.name}
                <button onClick={() => onSamplesChange(samples.filter((s2) => s2.id !== s.id))} className="ml-1 text-blue-400 hover:text-red-500">×</button>
              </span>
            ))}
          </div>
        )}
      </div>

      <div className="flex-1">
        <label className="block text-sm font-medium text-gray-600 mb-1">风格文字描述（可选）</label>
        <textarea
          value={description}
          onChange={(e) => onDescriptionChange(e.target.value)}
          placeholder="例如：简洁直接，少用被动语态，多用短句，避免冗余表达"
          className="w-full h-40 p-2 border border-gray-300 rounded text-sm resize-none focus:outline-none focus:ring-1 focus:ring-blue-400"
        />
      </div>
    </div>
  );
}
