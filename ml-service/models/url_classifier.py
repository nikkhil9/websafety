"""
URL Classification Model 
Uses trained Random Forest classifier for URL safety detection
"""

from urllib.parse import urlparse
import re
import logging
import joblib
import json
import os
import math

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class URLClassifier:
    """
    ML-based URL classification model for detecting malicious links
    
    Features:
    - Random Forest classifier (98.44% accuracy)
    - 20 extracted features per URL
    - 5 threat categories: safe, phishing, malware, spam, suspicious
    """
    
    def __init__(self):
        """Initialize the URL classification model"""
        try:
            logger.info("Loading URL classification model...")
            
            # Load trained Random Forest model
            model_path = os.path.join(os.path.dirname(__file__), "websafety-url-v1")
            
            self.model = joblib.load(os.path.join(model_path, "model.pkl"))
            
            # Load label mapping
            with open(os.path.join(model_path, "label_mapping.json"), 'r') as f:
                self.label_to_id = json.load(f)
                self.id_to_label = {v: k for k, v in self.label_to_id.items()}
            
            # Load feature config
            with open(os.path.join(model_path, "feature_config.json"), 'r') as f:
                config = json.load(f)
                self.feature_names = config['feature_names']
            
            # Constants for feature extraction
            self.url_shorteners = ['bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd']
            self.suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.online']
            self.suspicious_keywords = [
                'login', 'verify', 'account', 'secure', 'update', 'confirm',
                'banking', 'paypal', 'ebay', 'amazon', 'suspended', 'limited'
            ]
            
            logger.info("✓ Trained Random Forest URL model loaded successfully!")
            logger.info(f"  Categories: {list(self.label_to_id.keys())}")
            logger.info(f"  Model accuracy: 98.44%")
            
        except Exception as e:
            logger.error(f"Error loading URL model: {e}")
            raise
    
    def _calculate_entropy(self, text):
        """Calculate Shannon entropy of a string"""
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
        entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
        return entropy
    
    def _extract_features(self, url):
        """Extract 20 features from URL"""
        try:
            parsed = urlparse(url)
            domain = parsed.netloc.lower()
            path = parsed.path.lower()
            full_url = url.lower()
            
            # Extract features in correct order
            ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
            
            features = {
                "url_length": len(url),
                "domain_length": len(domain),
                "path_length": len(path),
                "subdomain_count": domain.count('.'),
                "has_https": 1 if parsed.scheme == 'https' else 0,
                "has_ip": 1 if ip_pattern.match(domain) else 0,
                "suspicious_tld": 1 if any(domain.endswith(tld) for tld in self.suspicious_tlds) else 0,
                "special_char_count": sum(url.count(c) for c in ['@', '-', '_', '%', '&', '=', '?', '#']),
                "digit_count": sum(c.isdigit() for c in url),
                "is_shortener": 1 if any(s in domain for s in self.url_shorteners) else 0,
                "has_suspicious_keywords": 1 if any(kw in full_url for kw in self.suspicious_keywords) else 0,
                "domain_entropy": round(self._calculate_entropy(domain), 4),
                "path_entropy": round(self._calculate_entropy(path) if path else 0.0, 4),
                "dot_count": domain.count('.'),
                "hyphen_count": domain.count('-'),
                "has_port": 1 if ':' in domain else 0,
                "query_param_count": parsed.query.count('&') + (1 if parsed.query else 0),
                "has_double_slash": 1 if '//' in path else 0,
                "digit_ratio": round(sum(c.isdigit() for c in url) / len(url) if len(url) > 0 else 0, 4),
                "special_char_ratio": round(sum(url.count(c) for c in ['@', '-', '_', '%', '&', '=', '?', '#']) / len(url) if len(url) > 0 else 0, 4)
            }
            
            # Convert to feature vector in correct order
            feature_vector = [features[fname] for fname in self.feature_names]
            return feature_vector
            
        except Exception as e:
            logger.error(f"Error extracting features: {e}")
            return None
    
    def analyze(self, url):
        """
        Analyze URL for malicious content using ML model
        
        Args:
            url (str): URL to analyze
            
        Returns:
            dict: Analysis results with threat level and category scores
        """
        try:
            # Extract features
            features = self._extract_features(url)
            
            if features is None:
                return self._error_response()
            
            # Predict
            prediction = self.model.predict([features])[0]
            probabilities = self.model.predict_proba([features])[0]
            
            # Get category and confidence
            category = self.id_to_label[prediction]
            confidence = probabilities[prediction]
            
            # Create categories dict with all probabilities
            categories = {}
            for cat_name, cat_id in self.label_to_id.items():
                categories[cat_name] = round(probabilities[cat_id], 3)
            
            # Determine safety
            is_safe = category == "safe"
            
            # Determine threat level based on category and confidence
            if is_safe:
                threat_level = "safe"
            elif category in ["malware", "phishing"] and confidence > 0.7:
                threat_level = "high"
            elif category == "spam" and confidence > 0.8:
                threat_level = "medium"
            elif category == "suspicious":
                threat_level = "medium"
            else:
                threat_level = "low"
            
            # Overall score (confidence of predicted category)
            overall_score = confidence
            
            # Parse URL for domain info
            parsed = urlparse(url)
            
            return {
                "is_safe": is_safe,
                "threat_level": threat_level,
                "category": category,
                "confidence": round(confidence, 3),
                "categories": categories,
                "overall_score": round(overall_score, 3),
                "domain_info": {
                    "domain": parsed.netloc,
                    "has_https": parsed.scheme == 'https',
                    "path_length": len(parsed.path),
                    "url_length": len(url)
                },
                "model": "websafety-url-rf"
            }
            
        except Exception as e:
            logger.error(f"Error analyzing URL: {e}")
            return self._error_response(str(e))
    
    def _error_response(self, error=None):
        """Return error response"""
        return {
            "is_safe": True,
            "threat_level": "safe",
            "category": "unknown",
            "confidence": 0.0,
            "categories": {label: 0.0 for label in self.label_to_id.keys()},
            "overall_score": 0.0,
            "error": error if error else "Unknown error",
            "model": "websafety-url-rf"
        }
