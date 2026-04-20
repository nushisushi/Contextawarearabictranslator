# Context-Aware Arabic Translator - Local Setup Instructions

## Prerequisites

Before running this project locally, ensure you have the following installed:

- **Node.js** (version 18 or higher)
- **pnpm** package manager

To install pnpm if you don't have it:
```bash
npm install -g pnpm
```

## Installation Steps

### 1. Clone or Download the Project

Navigate to the project directory in your terminal:
```bash
cd path/to/context-aware-arabic-translator
```

### 2. Install Dependencies

Run the following command to install all required packages:
```bash
pnpm install
```

This will install all dependencies listed in `package.json`, including:
- React and React DOM
- React Router for navigation
- Tailwind CSS for styling
- Vite for development server

### 3. Start the Development Server

Run the development server:
```bash
pnpm run dev
```

The application will start and be available at:
```
http://localhost:5173
```

(The port number may vary if 5173 is already in use)

### 4. Access the Application

Open your web browser and navigate to the URL shown in your terminal (typically `http://localhost:5173`)

## Project Structure

```
src/
├── app/
│   ├── App.tsx              # Main application component with router
│   ├── routes.tsx           # Route configuration
│   └── components/
│       ├── TranslatorInput.tsx   # Input page component
│       └── TranslatorResult.tsx  # Results page component
├── styles/
│   ├── theme.css            # Theme and design tokens
│   └── fonts.css            # Font imports
└── imports/                 # Asset imports
```

## ⚠️ IMPORTANT: Prerequisites

**This application requires trained model files that are NOT included in the repository.**

Before running the application, you must:
1. Train an Arabic dialect classifier using the IADD dataset
2. Save the trained models as pickle files in the `backend/` directory

See `backend/TRAINING_GUIDE.md` for detailed training instructions.

## Setting Up the Backend

This application requires a Python backend for dialect classification.

### 1. Train Your Model (Required First!)

**You must complete this step before the backend will work.**

Train your classifier using your training script and the IADD dataset. At the end of training, save the models:

```python
import pickle

# Save to backend directory
with open('backend/vectorizer.pkl', 'wb') as f:
    pickle.dump(vectorizer, f)
    
with open('backend/dialect_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

For detailed training instructions, see: `backend/TRAINING_GUIDE.md`

### 2. Verify Model Files Exist

```bash
ls backend/*.pkl
```

You should see:
- `backend/vectorizer.pkl`
- `backend/dialect_model.pkl`

### 3. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 4. Run the Backend API

```bash
cd backend
python api.py
```

The backend will run on `http://localhost:5000`

If you see "ERROR: Model files not found", you need to complete step 1 first.

## How to Use the Application

### Running Both Frontend and Backend

**Terminal 1 - Backend:**
```bash
cd backend
python api.py
```

**Terminal 2 - Frontend:**
```bash
pnpm run dev
```

### Using the App

1. **Enter Text**: On the home page, paste or type Arabic text into the text area
2. **Translate**: Click the "Translate" button
3. **View Results**: You'll be redirected to the results page showing:
   - Detected Arabic dialect (Egyptian, Levantine, Gulf, Iraqi, or Maghrebi)
   - Dialect code (EGY, LEV, GLF, IRQ, MGH)
   - Confidence score (how certain the model is)
   - Original text
   - Translation (currently echoes back the original)
4. **Translate Another**: Click "Translate Another" to return to the input page

## Building for Production

To create a production build:
```bash
pnpm run build
```

The optimized files will be generated in the `dist/` directory.

To preview the production build locally:
```bash
pnpm run preview
```

## Notes

- The dialect classification uses a trained Logistic Regression model on the IADD/DART dataset
- The model classifies Arabic text into 5 dialects: Egyptian, Levantine, Gulf, Iraqi, and Maghrebi
- Translation functionality is currently a placeholder (echoes back the original text)
- To add real translation, integrate a translation API or model in the backend

## Troubleshooting

### Port Already in Use
**Frontend:** If port 5173 is already in use, Vite will automatically try the next available port. Check your terminal output for the correct URL.

**Backend:** If port 5000 is in use, change it in `backend/api.py`:
```python
app.run(port=5001, debug=True)
```
Then update the fetch URL in `src/app/components/TranslatorInput.tsx` to match.

### Backend Connection Error
If you see "Failed to classify dialect" alert:
1. Make sure the backend is running (`python backend/api.py`)
2. Check that it's accessible at `http://localhost:5000`
3. Verify models are loaded (check terminal output when starting backend)

### Models Not Found
If the backend shows "Model files not found":
1. Run your training script first
2. Make sure it saves `vectorizer.pkl` and `dialect_model.pkl` in the `backend/` directory
3. Restart the backend API

### Dependencies Not Installing
Make sure you're using pnpm instead of npm or yarn:
```bash
pnpm install
```

### Module Not Found Errors
Clear the node_modules and reinstall:
```bash
rm -rf node_modules
pnpm install
```

## Technology Stack

- **React** 18.3.1 - UI framework
- **React Router** 7.13.0 - Client-side routing
- **Tailwind CSS** 4.1.12 - Utility-first CSS framework
- **Vite** 6.3.5 - Build tool and dev server
- **TypeScript** - Type safety (via .tsx files)

## Support

For issues or questions about running this project locally, please refer to the official documentation:
- [Vite Documentation](https://vitejs.dev/)
- [React Router Documentation](https://reactrouter.com/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
