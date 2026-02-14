# ML Service

Python-based Machine Learning service for Web Safety content analysis.

## Features

- **Text Analysis**: Toxic content detection using Hugging Face Transformers
- **Image Analysis**: NSFW and unsafe content detection (placeholder - to be implemented)
- **URL Analysis**: Malicious link detection using heuristics and ML

## Setup

### 1. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note**: First installation will download ML models (~500MB). This may take a few minutes.

### 3. Configure Environment

```bash
# Copy example env file
copy .env.example .env

# Edit .env if needed (optional)
```

### 4. Run the Service

```bash
python app.py
```

The service will start on `http://localhost:5001`

## Testing

### Run Test Script

```bash
# In a new terminal (keep server running)
python test_api.py
```

### Manual Testing with curl

**Text Analysis:**
```bash
curl -X POST http://localhost:5001/analyze/text ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"This is a test message\"}"
```

**URL Analysis:**
```bash
curl -X POST http://localhost:5001/analyze/url ^
  -H "Content-Type: application/json" ^
  -d "{\"url\": \"https://example.com\"}"
```

**Image Analysis:**
```bash
curl -X POST http://localhost:5001/analyze/image ^
  -F "image=@path/to/image.jpg"
```

## API Endpoints

### GET `/`
Health check endpoint
- **Response**: Service status and available endpoints

### POST `/analyze/text`
Analyze text for toxic content
- **Request Body**: `{"text": "string to analyze"}`
- **Response**: Threat level, categories, and scores

### POST `/analyze/image`
Analyze image for unsafe content
- **Request**: `multipart/form-data` with `image` file OR JSON with `image_base64`
- **Response**: Threat level, categories, and scores
- **Note**: Currently using placeholder model

### POST `/analyze/url`
Analyze URL for malicious content
- **Request Body**: `{"url": "https://example.com"}`
- **Response**: Threat level, categories, domain info, and scores

## Response Format

All analysis endpoints return:
```json
{
  "is_safe": true/false,
  "threat_level": "safe" | "low" | "medium" | "high",
  "categories": {
    "category1": 0.0-1.0,
    "category2": 0.0-1.0
  },
  "overall_score": 0.0-1.0
}
```

## Models Used

### Text Classification
- **Model**: `unitary/toxic-bert` from Hugging Face
- **Categories**: toxic, severe_toxic, obscene, threat, insult, hate
- **Fallback**: Sentiment analysis model

### Image Classification (TODO)
- **Current**: Placeholder implementation
- **Recommended**: NudeNet, Falconsai/nsfw_image_detection
- See `models/image_classifier.py` for implementation options

### URL Classification
- **Method**: Heuristic-based feature extraction
- **Features**: URL length, special chars, TLD, keywords, HTTPS
- **Enhancement**: Can add Google Safe Browsing API or VirusTotal

## Troubleshooting

### ModuleNotFoundError: No module named 'transformers'
Run: `pip install -r requirements.txt`

### Model download fails
- Check internet connection
- Models are downloaded from Hugging Face on first run
- Try running again - download will resume

### Port 5001 already in use
Change port in `.env` file:
```
PORT=5002
```

### Out of memory when loading models
- Close other applications
- Models require ~2-4GB RAM
- Consider using smaller models

## Next Steps

1. **Implement Image Classifier**: Replace placeholder with actual NSFW detection
2. **Add API Keys**: Integrate Google Safe Browsing for URL checking
3. **Optimize Performance**: Add caching and batch processing
4. **Add More Models**: Video analysis, audio analysis

## Project Structure

```
ml-service/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── test_api.py              # API test script
├── models/
│   ├── __init__.py
│   ├── text_classifier.py   # Text analysis model
│   ├── image_classifier.py  # Image analysis model (placeholder)
│   └── url_classifier.py    # URL analysis model
└── README.md                # This file
```
