import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from models import TextClassifier, ImageClassifier, URLClassifier

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize models
logger.info("Initializing ML models...")
try:
    text_classifier = TextClassifier()
    logger.info("Text classifier initialized")
except Exception as e:
    logger.error(f"Failed to initialize text classifier: {e}")
    text_classifier = None

try:
    image_classifier = ImageClassifier()
    logger.info("Image classifier initialized")
except Exception as e:
    logger.error(f"Failed to initialize image classifier: {e}")
    image_classifier = None

try:
    url_classifier = URLClassifier()
    logger.info("URL classifier initialized")
except Exception as e:
    logger.error(f"Failed to initialize URL classifier: {e}")
    url_classifier = None

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "online",
        "service": "Web Safety ML Service",
        "models": {
            "text": text_classifier is not None,
            "image": image_classifier is not None,
            "url": url_classifier is not None
        }
    })

@app.route('/analyze/text', methods=['POST'])
def analyze_text():
    """Analyze text for toxic content"""
    if not text_classifier:
        return jsonify({"error": "Text classification model not available"}), 503
    
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    result = text_classifier.analyze(data['text'])
    return jsonify(result)

@app.route('/analyze/image', methods=['POST'])
def analyze_image():
    """Analyze image for unsafe content"""
    if not image_classifier:
        return jsonify({"error": "Image classification model not available"}), 503
    
    # Handle file upload
    if 'image' in request.files:
        result = image_classifier.analyze_file(request.files['image'])
        return jsonify(result)
    
    # Handle base64 JSON
    data = request.get_json(silent=True)
    if data and 'image_base64' in data:
        result = image_classifier.analyze_base64(data['image_base64'])
        return jsonify(result)
        
    return jsonify({"error": "No image provided"}), 400

@app.route('/analyze/url', methods=['POST'])
def analyze_url():
    """Analyze URL for malicious content"""
    if not url_classifier:
        return jsonify({"error": "URL classification model not available"}), 503
    
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "No URL provided"}), 400
    
    result = url_classifier.analyze(data['url'])
    return jsonify(result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)
