# Backend API for Arabic Dialect Classification

This directory contains the Flask backend that serves an Arabic dialect classifier.

## ⚠️ IMPORTANT: Model Files Required

**This backend requires trained model files that are NOT included in this repository.**

You must train your own classifier model and place the following files in this `backend/` directory:
- `vectorizer.pkl` - TF-IDF vectorizer
- `dialect_model.pkl` - Trained classification model

## Setup

### 1. Train Your Model First

You need to train a dialect classifier using the IADD dataset before this backend will work.

**Training Script Example:**

Create a separate Python script (e.g., `train_classifier.py`) based on the code you provided. At the end of your training script, add these lines to save the models:

```python
import pickle

# After training your model (after model.fit(...)), add:
# Save to the backend directory
with open('backend/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
    
with open('backend/dialect_model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Models saved successfully!")
```

**Required Dataset:**
- Download the IADD dataset from: https://github.com/JihadZa/IADD
- Use the DART subset for best results
- Train with TF-IDF vectorizer (char n-grams 3-5) and Logistic Regression

### 2. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 3. Verify Model Files Exist

Make sure these files are in the `backend/` directory:
```bash
ls -la backend/
# Should show:
# vectorizer.pkl
# dialect_model.pkl
```

### 4. Run the API

```bash
python api.py
```

The API will start on `http://localhost:5000`

## API Endpoints

### POST /classify
Classifies Arabic text into one of 5 dialect categories.

**Request:**
```json
{
  "text": "إزيك يا معلم"
}
```

**Response:**
```json
{
  "dialect": "Egyptian",
  "dialect_code": "EGY",
  "confidence": 0.92,
  "translation": "إزيك يا معلم",
  "all_probabilities": {
    "Egyptian": 0.92,
    "Levantine": 0.04,
    "Gulf": 0.02,
    "Iraqi": 0.01,
    "Maghrebi": 0.01
  }
}
```

### GET /health
Check if the API is running and models are loaded.

**Response:**
```json
{
  "status": "ok",
  "models_loaded": true
}
```

## Supported Dialects

- **EGY** - Egyptian (مصري)
- **LEV** - Levantine (شامي)
- **GLF** - Gulf (خليجي)
- **IRQ** - Iraqi (عراقي)
- **MGH** - Maghrebi (مغربي)

## Testing

Test the API with curl:

```bash
curl -X POST http://localhost:5000/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "إزيك يا معلم"}'
```

## Troubleshooting

**Models not found error:**
- Make sure you've run your training script and saved the pickle files
- Check that `vectorizer.pkl` and `dialect_model.pkl` exist in the `backend/` directory

**CORS errors:**
- The API has CORS enabled for all origins
- Make sure the frontend is calling `http://localhost:5000` (not https)

**Port already in use:**
- Change the port in `api.py`: `app.run(port=5001, debug=True)`
- Update the frontend URL in `TranslatorInput.tsx` to match
