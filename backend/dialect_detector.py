import pandas as pd
import numpy as np
import re
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

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
        with open('vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)

        with open('dialect_model.pkl', 'rb') as f:
            model = pickle.load(f)

        print("✓ Dialect detector models loaded successfully")
        return True
    except FileNotFoundError as e:
        print(f"ERROR: Model files not found - {e}")
        print("You need to train the model first using the training data")
        return False

# NEW: checks whether the input is mostly Arabic script
ARABIC_CHAR_RE = re.compile(r"[\u0600-\u06FF]")

# NEW: checks whether a character is Arabic script
ARABIC_CHAR_RE = re.compile(r"[\u0600-\u06FF]")

def detect_dialect(text: str) -> str:
    """Detect the dialect of the input Arabic text"""
    text = str(text)

    # NEW: reject inputs that are mostly not Arabic script
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return "NON_ARABIC"

    arabic_letters = sum(bool(ARABIC_CHAR_RE.match(ch)) for ch in letters)
    arabic_ratio = arabic_letters / len(letters)

    # NEW: if too little Arabic is present, do not force a dialect prediction
    if arabic_ratio < 0.35:
        return "NON_ARABIC"

    text_clean = normalize_arabic(text)

    # NEW: if normalization strips everything out, treat it as non-Arabic
    if not text_clean:
        return "NON_ARABIC"

    text_vectorized = vectorizer.transform([text_clean])
    return model.predict(text_vectorized)[0]

def get_dialect_confidence(text: str) -> dict:
    """Get confidence scores for all dialects"""
    if vectorizer is None or model is None:
        raise ValueError("Models not loaded. Call load_models() first.")

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
