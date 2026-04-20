from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import re
import os

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# Load your saved models
# NOTE: These files are NOT included in the repository.
# You must train your own model first using the IADD dataset.
# See TRAINING_GUIDE.md for instructions.
try:
    with open('vectorizer.pkl', 'rb') as f:
        vectorizer = pickle.load(f)

    with open('dialect_model.pkl', 'rb') as f:
        model = pickle.load(f)

    print("✓ Models loaded successfully")
except FileNotFoundError as e:
    print("\n" + "="*60)
    print("ERROR: Model files not found!")
    print("="*60)
    print("\nThe following files are required but missing:")
    print("  - vectorizer.pkl")
    print("  - dialect_model.pkl")
    print("\nThese files are NOT included in the repository.")
    print("You must train your own classifier model first.")
    print("\nSee backend/TRAINING_GUIDE.md for instructions.")
    print("="*60 + "\n")
    vectorizer = None
    model = None

# Same normalization function from your training code
def normalize_arabic(text):
    """Normalize Arabic text (must match training preprocessing exactly)"""
    text = str(text)
    text = re.sub(r"[\u064B-\u0652]", "", text)  # Remove diacritics
    text = re.sub(r"[أإآ]", "ا", text)           # Normalize Alif
    text = re.sub(r"ى", "ي", text)              # Normalize Yeh
    text = re.sub(r"ة", "ه", text)              # Normalize Teh Marbuta
    text = re.sub(r"[^\u0621-\u064A\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Map model predictions to full dialect names
DIALECT_MAP = {
    'EGY': 'Egyptian',
    'LEV': 'Levantine',
    'GLF': 'Gulf',
    'IRQ': 'Iraqi',
    'MGH': 'Maghrebi'
}

@app.route('/classify', methods=['POST'])
def classify_dialect():
    """Classify Arabic text into dialect categories"""

    if vectorizer is None or model is None:
        return jsonify({
            'error': 'Models not loaded. Train and save models first.'
        }), 500

    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    try:
        # Preprocess (same as training)
        text_clean = normalize_arabic(text)

        if not text_clean:
            return jsonify({'error': 'Text contains no valid Arabic characters'}), 400

        # Vectorize
        text_tfidf = vectorizer.transform([text_clean])

        # Predict
        prediction = model.predict(text_tfidf)[0]
        probabilities = model.predict_proba(text_tfidf)[0]

        # Get confidence score
        confidence = float(max(probabilities))

        # Get all class probabilities for debugging
        class_probs = {
            DIALECT_MAP.get(cls, cls): float(prob)
            for cls, prob in zip(model.classes_, probabilities)
        }

        return jsonify({
            'dialect': DIALECT_MAP.get(prediction, prediction),
            'dialect_code': prediction,
            'confidence': confidence,
            'translation': text,  # For now, echo back (add real translation later)
            'all_probabilities': class_probs  # Optional: see all dialect scores
        })

    except Exception as e:
        return jsonify({'error': f'Classification error: {str(e)}'}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Check if API and models are ready"""
    return jsonify({
        'status': 'ok' if (vectorizer and model) else 'models_not_loaded',
        'models_loaded': vectorizer is not None and model is not None
    })

if __name__ == '__main__':
    print("\n" + "="*50)
    print("Arabic Dialect Classifier API")
    print("="*50)
    print("Running on: http://localhost:5000")
    print("Endpoints:")
    print("  POST /classify - Classify Arabic text")
    print("  GET  /health   - Health check")
    print("\nMake sure you have:")
    print("  1. vectorizer.pkl (from training)")
    print("  2. dialect_model.pkl (from training)")
    print("="*50 + "\n")

    app.run(port=5000, debug=True)
