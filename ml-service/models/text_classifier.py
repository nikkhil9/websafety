"""
Text Classification Model
Uses YOUR custom-trained WebSafety model with Hinglish and Tenglish support!
"""

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import json
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TextClassifier:
    """
    Custom WebSafety text classification model
    Trained on multi-Indic-language dataset (English, Hinglish, Tenglish)
    """
    
    def __init__(self):
        """Initialize the custom text classification model"""
        try:
            # Path to YOUR custom model (NEW XLM-RoBERTa v3)
            model_path = os.path.join(
                os.path.dirname(__file__), 
                "websafety-text-v3"
            )
            
            logger.info(f"Loading custom WebSafety model from {model_path}...")
            
            # Load tokenizer and model
            self.tokenizer = AutoTokenizer.from_pretrained(model_path)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
            
            # Load label mapping (NEW format: {"safe": 0, "phishing": 1, ...})
            label_map_path = os.path.join(model_path, "label_mapping.json")
            with open(label_map_path, 'r') as f:
                label_to_id = json.load(f)  # {"safe": 0, "phishing": 1, ...}
                self.label2id = label_to_id
                self.id2label = {v: k for k, v in label_to_id.items()}  # Reverse mapping
            
            # Set model to evaluation mode
            self.model.eval()
            
            logger.info("✓ Custom WebSafety model loaded successfully!")
            logger.info(f"  Categories: {list(self.label2id.keys())}")
            
        except Exception as e:
            logger.error(f"Error loading custom model: {e}")
            logger.error("Falling back to generic model...")
            # Fallback to original implementation
            from transformers import pipeline
            self.classifier = pipeline("text-classification", model="unitary/toxic-bert", top_k=None)
            self.id2label = None
    
    
    def analyze(self, text):
        """
        Analyze text using YOUR custom model
        
        Args:
            text (str): Text to analyze
            
        Returns:
            dict: Analysis results with category, confidence, and safety status
        """
        try:
            # Use custom model if loaded
            if self.id2label is not None:
                # Tokenize input
                inputs = self.tokenizer(
                    text,
                    return_tensors="pt",
                    truncation=True,
                    max_length=512,
                    padding=True
                )
                
                # Get prediction
                with torch.no_grad():
                    outputs = self.model(**inputs)
                
                # Get probabilities
                probs = torch.softmax(outputs.logits, dim=-1)
                confidence = probs.max().item()
                predicted_class = probs.argmax(-1).item()
                category = self.id2label[predicted_class]
                
                # CONFIDENCE THRESHOLD: if model is uncertain, treat as safe
                # This prevents false positives like "hello" being flagged as hate speech
                # Model needs >75% confidence to flag as threat
                CONFIDENCE_THRESHOLD = 0.75
                if category != "safe" and confidence < CONFIDENCE_THRESHOLD:
                    logger.info(f"Low confidence ({confidence:.2f}) for '{category}' - defaulting to safe")
                    category = "safe"
                    confidence = 1.0 - confidence  # safe confidence is the inverse
                
                # Determine safety
                is_safe = category == "safe"
                
                # Map to threat level
                if is_safe:
                    threat_level = "safe"
                elif confidence > 0.85:
                    threat_level = "high"
                elif confidence > 0.70:
                    threat_level = "medium"
                else:
                    threat_level = "low"
                
                # Get all predictions for categories display
                top_probs, top_indices = torch.topk(probs[0], min(len(self.id2label), 7))
                
                # Create categories dict for frontend
                categories = {}
                for prob, idx in zip(top_probs, top_indices):
                    cat_name = self.id2label[idx.item()]
                    categories[cat_name] = float(prob.item())
                
                # CYBERBULLYING OVERRIDE: even if overall confidence is low,
                # flag as suspicious if cyberbullying score > 30%
                cyberbullying_score = categories.get('cyberbullying', 0.0)
                if is_safe and cyberbullying_score > 0.30:
                    logger.info(f"Cyberbullying score {cyberbullying_score:.2f} > 30% - flagging as suspicious")
                    is_safe = False
                    category = "cyberbullying"
                    confidence = cyberbullying_score
                    threat_level = "medium"
                
                # overall_score: threat score (0 if safe)
                overall_score = 0.0 if is_safe else confidence
                
                return {
                    "is_safe": is_safe,
                    "threat_level": threat_level,
                    "category": category,  # Primary prediction
                    "confidence": round(confidence, 3),
                    "overall_score": round(overall_score, 3),  # For frontend
                    "categories": categories,  # For frontend breakdown
                    "text_length": len(text),
                    "model": "websafety-xlm-roberta"
                }
            
            else:
                # Fallback to original toxic-bert logic
                predictions = self.classifier(text[:512])
                
                categories = {
                    "toxic": 0.0,
                    "severe_toxic": 0.0,
                    "obscene": 0.0,
                    "threat": 0.0,
                    "insult": 0.0,
                    "hate": 0.0
                }
                
                if isinstance(predictions[0], list):
                    for pred in predictions[0]:
                        label = pred['label'].lower()
                        score = pred['score']
                        
                        if 'toxic' in label:
                            categories['toxic'] = max(categories['toxic'], score)
                        if 'severe' in label:
                            categories['severe_toxic'] = max(categories['severe_toxic'], score)
                        if 'obscene' in label:
                            categories['obscene'] = max(categories['obscene'], score)
                        if 'threat' in label:
                            categories['threat'] = max(categories['threat'], score)
                        if 'insult' in label:
                            categories['insult'] = max(categories['insult'], score)
                        if 'hate' in label:
                            categories['hate'] = max(categories['hate'], score)
                
                overall_score = max(categories.values())
                is_safe = overall_score < 0.5
                
                return {
                    "is_safe": is_safe,
                    "threat_level": "high" if overall_score > 0.7 else "medium" if overall_score > 0.5 else "safe",
                    "categories": categories,
                    "overall_score": round(overall_score, 3),
                    "model": "fallback"
                }
            
        except Exception as e:
            logger.error(f"Error analyzing text: {e}")
            return {
                "is_safe": True,
                "threat_level": "safe",
                "error": str(e),
                "model": "error"
            }
