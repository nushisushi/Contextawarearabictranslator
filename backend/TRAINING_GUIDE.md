# Training Guide: Arabic Dialect Classifier

This guide explains how to train the classifier model required for this application.

## Prerequisites

You need the training code that was provided separately. The training script should include:

1. Data loading from IADD dataset
2. Arabic text normalization
3. TF-IDF vectorization with char n-grams (3-5)
4. Logistic Regression model training

## Step-by-Step Training Process

### 1. Get the IADD Dataset

Download from: https://github.com/JihadZa/IADD

The dataset contains Arabic text labeled with regional dialects:
- **EGY** - Egyptian
- **LEV** - Levantine
- **GLF** - Gulf
- **IRQ** - Iraqi
- **MGH** - Maghrebi

### 2. Install Training Dependencies

```bash
pip install pandas scikit-learn matplotlib seaborn
```

### 3. Run Your Training Script

The training script should include these key components:

```python
import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pickle

# Load IADD dataset
df = pd.read_json("datasets/IADD.json")
df = df[df['DataSource'] == 'DART']

# Arabic normalization function
def normalize_arabic(text):
    text = str(text)
    text = re.sub(r"[\u064B-\u0652]", "", text)  # Remove diacritics
    text = re.sub(r"[أإآ]", "ا", text)           # Normalize Alif
    text = re.sub(r"ى", "ي", text)              # Normalize Yeh
    text = re.sub(r"ة", "ه", text)              # Normalize Teh Marbuta
    text = re.sub(r"[^\u0621-\u064A\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

# Preprocess
df['text_clean'] = df['Sentence'].apply(normalize_arabic)

# Sample and split
df_sampled = df.sample(frac=1, random_state=42).groupby('Region', group_keys=False).head(5000)
X_train, X_test, y_train, y_test = train_test_split(
    df_sampled['text_clean'], 
    df_sampled['Region'], 
    test_size=0.2, 
    stratify=df_sampled['Region'],
    random_state=42
)

# Vectorize
vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5), max_features=25000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# Train
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_tfidf, y_train)

# Evaluate
y_pred = model.predict(X_test_tfidf)
print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")

# SAVE THE MODELS (IMPORTANT!)
with open('backend/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
    
with open('backend/dialect_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("✓ Models saved to backend/vectorizer.pkl and backend/dialect_model.pkl")
```

### 4. Verify Model Files

After training, check that the files were created:

```bash
ls -lh backend/*.pkl
```

You should see:
- `backend/vectorizer.pkl` (~several MB)
- `backend/dialect_model.pkl` (~hundreds of KB)

### 5. Test the Backend

Now you can start the Flask API:

```bash
cd backend
python api.py
```

Test it with curl:
```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "إزيك يا معلم"}'
```

Expected response:
```json
{
  "dialect": "Egyptian",
  "dialect_code": "EGY",
  "confidence": 0.92,
  ...
}
```

## Expected Model Performance

With the IADD/DART dataset and the recommended configuration:
- **Accuracy**: ~85-90% on test set
- **Training time**: 2-5 minutes on modern hardware
- **Model size**: ~5-10 MB total for both pickle files

## Troubleshooting Training

**Low accuracy (<70%):**
- Check that Arabic normalization is applied correctly
- Verify you're using the DART subset
- Ensure balanced sampling across all 5 dialects

**Out of memory errors:**
- Reduce `max_features` in TfidfVectorizer
- Reduce sample size per region (try 3000 instead of 5000)

**FileNotFoundError when saving:**
- Make sure you're running from the project root
- The `backend/` directory must exist
- Use the correct path: `'backend/vectorizer.pkl'`

## Model Updates

To retrain with new data or different parameters:
1. Delete the old `.pkl` files
2. Modify your training script
3. Run training again
4. Restart the Flask API to load new models
