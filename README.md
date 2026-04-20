# Context-Aware Arabic Translator

A web application for detecting Arabic dialects and translating Arabic text. Built with React, TypeScript, Tailwind CSS, and a Python Flask backend.

## Features

- **Dialect Detection**: Classifies Arabic text into 5 regional dialects:
  - Egyptian (مصري)
  - Levantine (شامي)
  - Gulf (خليجي)
  - Iraqi (عراقي)
  - Maghrebi (مغربي)

- **Confidence Scoring**: Shows how confident the model is in its prediction
- **Clean UI**: Simple, responsive interface for text input and results display
- **Real-time Classification**: Instant dialect detection using trained ML model

## ⚠️ Important: Model Files Required

**This repository does NOT include the trained model files.**

Before running the application, you must:

1. Train an Arabic dialect classifier using the IADD dataset
2. Save the trained model files in the `backend/` directory:
   - `backend/vectorizer.pkl` (TF-IDF vectorizer)
   - `backend/dialect_model.pkl` (trained classifier)

See **[backend/TRAINING_GUIDE.md](backend/TRAINING_GUIDE.md)** for step-by-step training instructions.

## Quick Start

### Prerequisites

- **Node.js** 18+ and **pnpm**
- **Python** 3.8+ and **pip**
- **Trained model files** (see above)

### 1. Train the Model First

Follow the instructions in `backend/TRAINING_GUIDE.md` to:
- Download the IADD dataset
- Train your classifier
- Save the model files to `backend/`

### 2. Install Dependencies

**Frontend:**
```bash
pnpm install
```

**Backend:**
```bash
cd backend
pip install -r requirements.txt
```

### 3. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
python api.py
```

**Terminal 2 - Frontend:**
```bash
pnpm run dev
```

Open your browser to the URL shown (typically `http://localhost:5173`)

## Project Structure

```
.
├── src/
│   ├── app/
│   │   ├── App.tsx                    # Main app with router
│   │   ├── routes.tsx                 # Route configuration
│   │   └── components/
│   │       ├── TranslatorInput.tsx    # Input page
│   │       └── TranslatorResult.tsx   # Results page
│   └── styles/
│       ├── theme.css                  # Design tokens
│       └── fonts.css                  # Font imports
├── backend/
│   ├── api.py                         # Flask API server
│   ├── requirements.txt               # Python dependencies
│   ├── TRAINING_GUIDE.md             # How to train the model
│   ├── README.md                      # Backend documentation
│   ├── vectorizer.pkl                 # ⚠️ NOT INCLUDED - must train
│   └── dialect_model.pkl              # ⚠️ NOT INCLUDED - must train
├── LOCAL_SETUP.md                     # Detailed setup guide
└── README.md                          # This file
```

## Technology Stack

**Frontend:**
- React 18.3.1
- TypeScript
- React Router 7.13.0
- Tailwind CSS 4.1.12
- Vite 6.3.5

**Backend:**
- Python 3.8+
- Flask 3.0.0
- scikit-learn 1.5.0
- pandas, numpy

## API Endpoints

### POST /classify
Classifies Arabic text into dialect categories.

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
Check API status and model loading.

## Current Limitations

- **Translation**: Currently echoes back the original text. Real translation would require integrating a separate translation model or API.
- **Model Required**: You must train and provide your own classifier model.
- **Dataset**: Requires the IADD/DART dataset for training.

## Troubleshooting

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed troubleshooting steps.

**Common Issues:**

- **"Model files not found"**: You need to train the model first (see `backend/TRAINING_GUIDE.md`)
- **"Failed to classify dialect"**: Make sure the backend is running on `http://localhost:5000`
- **CORS errors**: Backend has CORS enabled; ensure you're using `http://` not `https://`

## Dataset

This application is designed to work with the **IADD (Inter-Arabic Dialect Dataset)**, specifically the DART subset.

- **Source**: https://github.com/JihadZa/IADD
- **License**: Check the IADD repository for licensing terms
- **Size**: ~25,000 sentences across 5 Arabic dialects

## License

[Add your license here]

## Acknowledgments

- IADD dataset creators for providing dialect-labeled Arabic text
- Built as part of CS 329 coursework
