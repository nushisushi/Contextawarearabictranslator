import pandas as pd
import numpy as np
import re
from pathlib import Path
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

BASE_DIR = Path(__file__).resolve().parent
VECTORIZER_PATH = BASE_DIR / "vectorizer.pkl"
MODEL_PATH = BASE_DIR / "dialect_model.pkl"

# --- ARABIC NORMALIZATION ---
def normalize_arabic(text):
    text = str(text)
    text = re.sub(r"[\u064B-\u0652]", "", text)
    text = re.sub(r"[أإآ]", "ا", text)
    text = re.sub(r"ى", "ي", text)
    text = re.sub(r"ة", "ه", text)
    text = re.sub(r"[^\u0621-\u064A\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Global variables for model and vectorizer
vectorizer = None
model = None

def load_models():
    """Load the trained vectorizer and model"""
    global vectorizer, model

    try:
        with open(VECTORIZER_PATH, 'rb') as f:
            vectorizer = pickle.load(f)

        with open(MODEL_PATH, 'rb') as f:
            model = pickle.load(f)

        print("✓ Dialect detector models loaded successfully")
        return True
    except FileNotFoundError as e:
        print(f"ERROR: Model files not found - {e}")
        print(f"Expected files at: {VECTORIZER_PATH} and {MODEL_PATH}")
        print("You need to train the model first using the training data")
        return False

def _ensure_models_loaded():
    """Load models lazily if they are not already loaded"""
    global vectorizer, model

    if vectorizer is None or model is None:
        ok = load_models()
        if not ok:
            raise FileNotFoundError(
                f"Could not load model files from {BASE_DIR}. "
                "Make sure vectorizer.pkl and dialect_model.pkl are in backend/."
            )

# NEW: checks whether a character is Arabic script
ARABIC_CHAR_RE = re.compile(r"[\u0600-\u06FF]")

def detect_dialect(text: str) -> str:
    """Detect the dialect of the input Arabic text"""
    _ensure_models_loaded()

    text = str(text)

    # Reject inputs that are mostly not Arabic script
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return "NON_ARABIC"

    arabic_letters = sum(bool(ARABIC_CHAR_RE.match(ch)) for ch in letters)
    arabic_ratio = arabic_letters / len(letters)

    if arabic_ratio < 0.35:
        return "NON_ARABIC"

    text_clean = normalize_arabic(text)

    if not text_clean:
        return "NON_ARABIC"

    text_vectorized = vectorizer.transform([text_clean])
    return model.predict(text_vectorized)[0]

def get_dialect_confidence(text: str) -> dict:
    """Get confidence scores for all dialects"""
    _ensure_models_loaded()

    if detect_dialect(text) == "NON_ARABIC":
        dialect_probs = {
            dialect: 0.0
            for dialect in model.classes_
        }
        return {
            'dialect': "NOT ARABIC",
            'confidence': 1.0,
            'all_probabilities': dialect_probs
        }

    text_clean = normalize_arabic(text)
    text_vectorized = vectorizer.transform([text_clean])

    prediction = model.predict(text_vectorized)[0]
    probabilities = model.predict_proba(text_vectorized)[0]

    # Map probabilities to dialect names
    dialect_probs = {
        dialect: float(prob)
        for dialect, prob in zip(model.classes_, probabilities)
    }

    return {
        'dialect': prediction,
        'confidence': float(max(probabilities)),
        'all_probabilities': dialect_probs
    }
