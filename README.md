# Context-Aware Arabic Translator

A simple web application for Arabic dialect detection and translation. Built with React, TypeScript, Tailwind CSS, and React Router.

## Features

- **Text Input**: Clean interface for entering Arabic text
- **Dialect Detection**: Displays detected Arabic dialect (Maghrebi, Egyptian, Gulf, or Levantine)
- **Translation Display**: Shows the translated text
- **Loading States**: Visual feedback during translation
- **Responsive Design**: Works on desktop and mobile devices

## Quick Start

### Prerequisites

- **Node.js** 18+ 
- **pnpm** package manager

### Installation

1. **Install dependencies:**
```bash
pnpm install
```

2. **Start the development server:**
```bash
pnpm run dev
```

3. **Open your browser** to the URL shown (typically `http://localhost:5173`)

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
├── LOCAL_SETUP.md                     # Detailed setup guide
└── README.md                          # This file
```

## Technology Stack

- **React** 18.3.1 - UI framework
- **TypeScript** - Type safety
- **React Router** 7.13.0 - Client-side routing
- **Tailwind CSS** 4.1.12 - Utility-first CSS framework
- **Vite** 6.3.5 - Build tool and dev server

## How It Works

1. User enters text on the input page
2. Clicking "Translate" shows a loading animation
3. Results page displays:
   - Detected Arabic dialect
   - Original text
   - Translation

## Current Implementation

This is a **frontend-only demo** with mock functionality:
- Dialect detection is randomized among the four supported dialects
- Translation is placeholder text
- 2-second simulated loading delay

## Integrating Real Translation

To connect real translation services, you would need to:

1. Set up a backend API (Python Flask, Node.js Express, etc.)
2. Integrate an Arabic dialect classifier
3. Connect to a translation service (Google Translate API, Hugging Face models, etc.)
4. Update `src/app/components/TranslatorInput.tsx` to call your API

## Building for Production

To create a production build:
```bash
pnpm run build
```

The optimized files will be in the `dist/` directory.

## Troubleshooting

See [LOCAL_SETUP.md](LOCAL_SETUP.md) for detailed troubleshooting steps.

**Common Issues:**

- **Dependencies not installing**: Use `pnpm install` (not npm or yarn)
- **Port already in use**: Vite will automatically use the next available port
- **Module errors**: Clear node_modules and reinstall: `rm -rf node_modules && pnpm install`

## License

[Add your license here]
