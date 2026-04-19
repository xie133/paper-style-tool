import { useState, useRef } from "react";
import StylePanel from "./components/StylePanel";
import InputPanel from "./components/InputPanel";
import ResultPanel from "./components/ResultPanel";
import { streamProcess } from "./api";

export default function App() {
  const [samples, setSamples] = useState([]);
  const [styleDescription, setStyleDescription] = useState("");
  const [paperText, setPaperText] = useState("");
  const [mode, setMode] = useState("");
  const [instruction, setInstruction] = useState("");
  const [result, setResult] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState("");
  const stopRef = useRef(null);

  function handleProcess() {
    if (isProcessing) {
      if (stopRef.current) stopRef.current();
      setIsProcessing(false);
      return;
    }
    setResult("");
    setError("");
    setIsProcessing(true);

    const stop = streamProcess(
      {
        text: paperText,
        mode,
        styleSamples: samples.map((s) => s.text),
        styleDescription,
        instruction,
      },
      (chunk) => setResult((prev) => prev + chunk),
      (err) => { setError(err); setIsProcessing(false); },
      () => setIsProcessing(false),
    );
    stopRef.current = stop;
  }

  return (
    <div className="flex flex-col h-screen bg-white">
      <header className="px-6 py-3 border-b border-gray-200 bg-gray-50">
        <h1 className="text-xl font-bold text-gray-800">论文风格助手</h1>
      </header>
      <main className="flex flex-1 overflow-hidden">
        <div className="w-64 shrink-0 overflow-y-auto">
          <StylePanel
            samples={samples}
            onSamplesChange={setSamples}
            description={styleDescription}
            onDescriptionChange={setStyleDescription}
          />
        </div>
        <div className="flex-1 overflow-y-auto">
          <InputPanel
            text={paperText}
            onTextChange={setPaperText}
            mode={mode}
            onModeChange={setMode}
            instruction={instruction}
            onInstructionChange={setInstruction}
            onProcess={handleProcess}
            isProcessing={isProcessing}
          />
        </div>
        <div className="w-96 shrink-0 overflow-y-auto">
          <ResultPanel result={result} isProcessing={isProcessing} error={error} />
        </div>
      </main>
    </div>
  );
}
