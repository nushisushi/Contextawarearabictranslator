import { useState } from "react";
import { useNavigate } from "react-router";

export function TranslatorInput() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleTranslate = async () => {
    if (!text.trim()) return;

    setIsLoading(true);

    try {
      // Call Python backend for dialect classification
      const response = await fetch('http://localhost:5000/classify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: text })
      });

      if (!response.ok) {
        throw new Error('Classification failed');
      }

      const data = await response.json();

      navigate("/result", {
        state: {
          dialect: data.dialect,           // Egyptian, Levantine, Gulf, Iraqi, or Maghrebi
          dialectCode: data.dialect_code,  // EGY, LEV, GLF, IRQ, MGH
          translation: data.translation,   // Translation (currently echoes back)
          originalText: text,
          confidence: data.confidence      // Model confidence score
        }
      });
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to classify dialect. Make sure the Python backend is running on http://localhost:5000');
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl text-center mb-8 text-gray-800">
          Context-Aware Arabic Translator
        </h1>

        <div className="space-y-6">
          <div>
            <label htmlFor="text-input" className="block mb-2 text-gray-700">
              Enter text to translate:
            </label>
            <textarea
              id="text-input"
              value={text}
              onChange={(e) => setText(e.target.value)}
              className="w-full h-48 p-4 border-2 border-gray-300 rounded-lg focus:border-indigo-500 focus:outline-none resize-none"
              placeholder="Paste your text here..."
              disabled={isLoading}
            />
          </div>

          <button
            onClick={handleTranslate}
            disabled={!text.trim() || isLoading}
            className="w-full py-3 px-6 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          >
            {isLoading ? (
              <span className="flex items-center justify-center gap-2">
                <span className="inline-block w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                Translating...
              </span>
            ) : (
              "Translate"
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
