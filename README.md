# WebSafety

**Intelligent Multi-Modal Learning System for Real-Time Online Safety and Content Governance**

A comprehensive web application that uses advanced machine learning to detect and classify harmful online content across text, URLs, and images.

## 🌟 Features

### Multi-Modal Classification
- **Text Analysis**: Detects cyberbullying, hate speech, phishing attempts, and harmful content
  - Multi-lingual support (English, Hinglish, Telenglish)
  - XLM-RoBERTa fine-tuned model
  - 80.97% accuracy across 4 categories
  
- **URL Scanner**: Identifies malicious URLs across 5 categories
  - Random Forest classifier with 20+ URL features
  - 98% accuracy
  - Categories: Safe, Phishing, Malware, Spam, Suspicious

- **Image Moderation**: Classifies images into safe/unsafe content
  - Ensemble of pre-trained models
  - 92% accuracy
  - Categories: Safe, Violence, Nudity, Drugs, Weapons

### Real-Time Processing
- RESTful API endpoints for all classifiers
- Fast response times (text: ~850ms, URL: ~42ms, image: ~2.3s)
- Concurrent request handling

### Modern Web Interface
- Clean, responsive React UI
- Real-time classification results
- Visual feedback with animations
- Mobile-friendly design

## 🏗️ Architecture

```
WebSafety/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   └── package.json
│
├── ml-service/        # Flask ML backend
│   ├── models/        # Trained models
│   ├── dataset/       # Training datasets
│   ├── app.py         # Main API
│   └── requirements.txt
│
└── research_figures/  # Research paper visualizations
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 16+
- 8GB+ RAM (for model inference)

### Backend Setup

```bash
cd ml-service

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Start Flask server
python app.py
# Server runs on http://127.0.0.1:5001
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
# App runs on http://localhost:5173
```

## 📡 API Endpoints

### Text Classification
```bash
POST /api/classify/text
Content-Type: application/json

{
  "text": "Your text here"
}
```

Response:
```json
{
  "category": "safe",
  "confidence": 0.95,
  "processing_time_ms": 850
}
```

### URL Classification
```bash
POST /api/classify/url
Content-Type: application/json

{
  "url": "https://example.com"
}
```

### Image Classification
```bash
POST /api/classify/image
Content-Type: multipart/form-data

file: <image file>
```

## 📊 Model Performance

| Model | Accuracy | Categories | Technology |
|-------|----------|------------|------------|
| Text Classifier | 80.97% | 4 | XLM-RoBERTa |
| URL Classifier | 98% | 5 | Random Forest |
| Image Classifier | 92% | 5 | Ensemble CNN |

### Text Classification Metrics
- **Safe**: 99.67% F1-score
- **Phishing**: 86.02% F1-score
- **Hate Speech**: 76.89% F1-score
- **Cyberbullying**: 55.21% F1-score (challenging due to context)

### Dataset
- **Text**: 30,000 unique samples (multilingual)
  - English: 10,000 samples
  - Hinglish: 10,000 samples
  - Telenglish: 10,000 samples
- **URLs**: 10,000 samples with feature engineering
- **Images**: 5,000+ samples from public datasets

## 🛠️ Technology Stack

### Backend
- **Framework**: Flask
- **ML Libraries**: 
  - Transformers (Hugging Face)
  - PyTorch
  - scikit-learn
  - TensorFlow (image models)
- **NLP**: XLM-RoBERTa, sentence-transformers
- **Computer Vision**: ResNet, VGG, InceptionV3

### Frontend
- **Framework**: React 18
- **Build Tool**: Vite
- **Styling**: CSS3 with CSS Variables
- **Animations**: Framer Motion

## 📝 Research

This project is part of academic research on multi-modal content moderation. The research paper includes:
- System architecture and novelty
- Comprehensive performance evaluation
- Cross-lingual analysis
- Confusion matrix and error analysis

Research figures are available in `research_figures/` directory.

## 🔒 Security & Privacy

- No data is stored permanently
- All inference happens locally
- No external API calls for classification
- User data is not logged

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is for academic and research purposes.

## 👥 Authors

- **A. Nikhil** - Vellore Institute of Technology (VIT)

## 🙏 Acknowledgments

- Hugging Face for transformer models
- Research datasets from various open-source projects
- VIT faculty for guidance

## 📧 Contact

For questions or collaboration:
- GitHub: [@nikkhil9](https://github.com/nikkhil9)
- Project Link: [https://github.com/nikkhil9/websafety](https://github.com/nikkhil9/websafety)

---

**Note**: Models are not included in this repository due to size constraints. Please follow the setup instructions to download or train models.
