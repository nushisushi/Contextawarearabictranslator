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

## How to Use the Application

### Start the Development Server

```bash
pnpm run dev
```

The application will start at `http://localhost:5173`

### Using the App

1. **Enter Text**: On the home page, paste or type text into the text area
2. **Translate**: Click the "Translate" button
3. **View Results**: After a brief loading animation, you'll be redirected to the results page showing:
   - Detected Arabic dialect (Maghrebi, Egyptian, Gulf, or Levantine)
   - Original text
   - Translation
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

- This is a demo application with mock translation functionality
- The dialect detection is randomized for demonstration purposes
- To integrate real translation, you would need to connect to an actual Arabic translation API
- The loading delay is simulated (2 seconds) to demonstrate the loading state

## Troubleshooting

### Port Already in Use
If port 5173 is already in use, Vite will automatically try the next available port. Check your terminal output for the correct URL.

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
