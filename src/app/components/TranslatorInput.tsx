import { useState } from "react";
import { useNavigate } from "react-router";

export function TranslatorInput() {
  const [text, setText] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();

  const handleTranslate = async () => {
    if (!text.trim()) return;

    setIsLoading(true);

    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Mock translation result
    const dialects = ["Maghrebi", "Egyptian", "Gulf", "Levantine"];
    const randomDialect = dialects[Math.floor(Math.random() * dialects.length)];
    const mockTranslation = `This is a translated version of: ${text}`;

    navigate("/result", {
      state: {
        dialect: randomDialect,
        translation: mockTranslation,
        originalText: text
      }
    });
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
