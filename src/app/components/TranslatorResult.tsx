import { useLocation, useNavigate } from "react-router";
import { useEffect } from "react";

export function TranslatorResult() {
  const location = useLocation();
  const navigate = useNavigate();
  const { dialect, translation, originalText } = location.state || {};

  useEffect(() => {
    if (!dialect || !translation) {
      navigate("/");
    }
  }, [dialect, translation, navigate]);

  if (!dialect || !translation) {
    return null;
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4">
      <div className="w-full max-w-2xl bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-3xl text-center mb-8 text-gray-800">
          Translation Result
        </h1>

        <div className="space-y-6">
          <div className="bg-indigo-50 border-l-4 border-indigo-600 p-4 rounded">
            <p className="text-sm text-gray-600 mb-1">Detected Dialect:</p>
            <p className="text-2xl text-indigo-700">{dialect}</p>
          </div>

          <div>
            <p className="text-sm text-gray-600 mb-2">Original Text:</p>
            <div className="bg-gray-50 p-4 rounded border border-gray-200">
              <p className="text-gray-800">{originalText}</p>
            </div>
          </div>

          <div>
            <p className="text-sm text-gray-600 mb-2">Translation:</p>
            <div className="bg-green-50 p-4 rounded border border-green-200">
              <p className="text-gray-800">{translation}</p>
            </div>
          </div>

          <button
            onClick={() => navigate("/")}
            className="w-full py-3 px-6 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Translate Another
          </button>
        </div>
      </div>
    </div>
  );
}
