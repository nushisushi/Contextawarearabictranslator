from transformers import MarianMTModel, MarianTokenizer
import torch

MODEL_NAME = "Helsinki-NLP/opus-mt-ar-en"

# Global variables
tokenizer = None
model = None
device = None

def load_translation_model():
    """Load the OPUS-MT Arabic→English Model"""
    global tokenizer, model, device

    print("Loading translation model (this may take a moment)...")

    tokenizer = MarianTokenizer.from_pretrained(MODEL_NAME)
    model = MarianMTModel.from_pretrained(MODEL_NAME)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    print(f"✓ Translation model loaded successfully on {device}")
    return True

# NEW: lets the function accept either the classifier label or our existing category name
# Dialect Normalization Layer (Key Innovation)
DIALECT_LABEL_ALIASES = {
    "EGY": "EGY",
    "GLF": "GLF",
    "IRQ": "IRQ",
    "MSA": "MSA",
    "LEV": "LEV",
    "LAV": "LEV",
    "MGH": "MGH",
    "NOR": "MGH"
}

# Dialect Normalization Layer
DIALECT_NORMALIZATION = {
    "EGY": {
        # Negation
        "مش": "ليس",
        "مش ب": "لا",
        # Verbs
        "رايح": "ذاهب",
        "جاي": "قادم",
        "عايز": "أريد",
        "عاوزه": "أريده",
        # Phrases
        "مش تعبان": "لست متعبا",
        "مش فاهم": "لا أفهم",
        # Question words
        "فين": "أين",
        "ليه": "لماذا"
    },
    "LEV": {
        # Negation
        "مو": "ليس",
        "مش": "ليس",
        # Intent / desire
        "بدّي": "أريد",
        "بدي": "أريد",
        # Verbs
        "راح": "ذهب",
        "إجا": "جاء",
        # Location/question
        "وين": "أين",
        "ليش": "لماذا"
    },
    "GLF": {
        # Desire
        "أبغى": "أريد",
        "أبي": "أريد",
        # Negation
        "مو": "ليس",
        # Question
        "وين": "أين",
        "ليش": "لماذا"
    },
    "IRQ": {
        # Negation
        "ماكو": "لا يوجد",
        "مو": "ليس",
        # Verbs
        "أريد": "أريد",
        "أروح": "أذهب",
        # Question
        "وين": "أين",
        "ليش": "لماذا"
    },
    "MGH": {
        # Negation
        "ما": "لا",
        # Desire
        "نبغي": "نريد",
        "بغيت": "أردت",
        # Question
        "فين": "أين",
        "علاش": "لماذا",
        # NEW: common Maghrebi forms
        "دابا": "الآن",
        "بزاف": "كثيرا",
        "هاد": "هذا"
    }
}

def normalize_dialect(text: str, dialect: str):
    """
    Replace dialectal words with MSA equivalents.
    Returns normalized text + list of applied rules.
    """
    applied_rules = []

    # NEW: maps alternate dialect labels to the category names already used in DIALECT_NORMALIZATION
    dialect = DIALECT_LABEL_ALIASES.get(dialect, dialect)
    rules = DIALECT_NORMALIZATION.get(dialect, {})

     # NEW: start with the original full text so multi-word phrase rules can be applied before splitting into tokens
    normalized_text = text
    
    # NEW: apply phrase-level replacements first
    # This is necessary because text.split() would break "مش تعبان" into two separate tokens
    for source, target in rules.items():
        if " " in source and source in normalized_text:
            normalized_text = normalized_text.replace(source, target)
            applied_rules.append(f"{source} → {target}")

    tokens = normalized_text.split()

    rules = DIALECT_NORMALIZATION.get(dialect, {})
    tokens = text.split()

    normalized_tokens = []
    for token in tokens:
        if token in rules:
            normalized_tokens.append(rules[token])
            applied_rules.append(f"{token} → {rules[token]}")
        else:
            normalized_tokens.append(token)

    normalized_text = " ".join(normalized_tokens)
    return normalized_text, applied_rules

def translate_ar_to_en(text: str, max_length: int = 128):
    """
    Translate Arabic text to English using OPUS-MT.
    """
    if tokenizer is None or model is None:
        raise ValueError("Translation model not loaded. Call load_translation_model() first.")

    inputs = tokenizer(text, return_tensors="pt", padding=True).to(device)

    with torch.no_grad():
        translated = model.generate(
            **inputs,
            max_length=max_length,
            num_beams=5,
            early_stopping=True
        )

    return tokenizer.decode(translated[0], skip_special_tokens=True)

# Ambiguity Awareness
AMBIGUOUS_WORDS = {
    "راح": ["went", "will go"],
    "كان": ["was", "used to be"],
    "طلع": ["went out", "turned out", "appeared"]
}

def get_ambiguity_notes(text: str):
    """Identify potentially ambiguous words in the text"""
    notes = []
    for word, meanings in AMBIGUOUS_WORDS.items():
        if word in text:
            notes.append({
                "word": word,
                "possible_meanings": meanings
            })
    return notes
