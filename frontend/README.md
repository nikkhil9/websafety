# Web Safety Frontend

Beautiful React web application to showcase the Web Safety ML service.

## Features

- 🤖 **Text Analysis**: Detect toxic, hateful, and threatening content using AI
- 🔗 **URL Scanner**: Identify phishing and malicious URLs
- 📊 **Live Statistics**: Track scans and threats in real-time
- 🎨 **Modern UI**: Dark theme with animations and gradient effects
- 📱 **Responsive**: Works on desktop, tablet, and mobile

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Start ML Service (Required)

Make sure the ML service is running on port 5001:

```bash
cd ../ml-service
venv\Scripts\activate
python app.py
```

### 3. Start Frontend

```bash
npm run dev
```

The app will open at `http://localhost:3000`

## Usage

### Text Analysis
1. Click on "Text Analysis" tab
2. Enter text in the textarea
3. Click "Analyze Text"
4. View detailed threat analysis with category breakdown

### URL Scanner
1. Click on "URL Scanner" tab
2. Enter a URL
3. Click "Scan URL"
4. View security assessment and domain information

## Tech Stack

- **React 18**: UI framework
- **Vite**: Build tool
- **Axios**: HTTP client
- **CSS3**: Styling with modern features

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── Header.jsx          # App header with logo
│   │   ├── Header.css
│   │   ├── Stats.jsx           # Statistics cards
│   │   ├── Stats.css
│   │   ├── TextAnalyzer.jsx    # Text analysis UI
│   │   ├── URLScanner.jsx      # URL scanning UI
│   │   └── Analyzer.css        # Shared analyzer styles
│   ├── App.jsx                 # Main app component
│   ├── App.css
│   ├── main.jsx               # Entry point
│   └── index.css              # Global styles
├── index.html
├── package.json
└── vite.config.js             # Vite config with proxy
```

## API Integration

The frontend connects to the ML service through a proxy configured in `vite.config.js`:

- `/api/analyze/text` → `http://localhost:5001/analyze/text`
- `/api/analyze/url` → `http://localhost:5001/analyze/url`

## Demo

**Text Analysis:**
- Try: "Hello friend!" → Safe
- Try: "I hate you!" → High threat detected

**URL Scanner:**
- Try: "https://google.com" → Safe
- Try: "http://phishing-site.tk" → High threat

## Troubleshooting

### ML Service Connection Error
Make sure `python app.py` is running in the ml-service directory

### Port Already in Use
Change port in `vite.config.js`:
```js
server: { port: 3001 }
```

### Blank Page
Check browser console for errors. Make sure all dependencies are installed.

## Next Steps

- Add image analysis when ML model is ready
- Implement result history (requires backend)
- Add export reports feature
- Create browser extension integration

---

**Part of Web Safety Final Year Project**
