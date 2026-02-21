"""
Image Classification Model
Uses Computer Vision models for NSFW and unsafe content detection
"""

from PIL import Image
import io
import base64
import logging
import numpy as np
import hashlib
from functools import lru_cache

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImageClassifier:
    """
    Image classification model for detecting NSFW and unsafe content
    
    Note: For production use, consider:
    - NudeNet: https://github.com/notAI-tech/NudeNet
    - Yahoo OpenNSFW: Pre-trained NSFW detection
    - Clarifai API: Commercial solution
    
    For this implementation, we'll use a placeholder that can be replaced
    with actual models when ready.
    """
    
    def __init__(self):
        """Initialize the image classification models"""
        try:
            logger.info("Loading image classification models...")
            
            # Load NSFW detection model (works correctly)
            from transformers import pipeline
            logger.info("Loading NSFW detection model...")
            self.nsfw_detector = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
            
            # Load violence detection model
            # NOTE: jaranohaal/vit-base-violence-detection uses timm format (incompatible)
            # Using Falconsai violence model which loads correctly
            logger.info("Loading violence detection model...")
            try:
                self.violence_detector = pipeline(
                    "image-classification",
                    model="Falconsai/MobileNet_V2_Violence_Offensive"
                )
                logger.info("✓ Violence detection model loaded!")
            except Exception as ve:
                logger.warning(f"Violence model failed to load: {ve}")
                logger.warning("Violence detection will be disabled - only NSFW detection active")
                self.violence_detector = None
            
            self.model_loaded = True
            logger.info("Image classifier initialized successfully!")
            
            # Initialize result cache
            self.result_cache = {}
            self.cache_max_size = 100
            
        except Exception as e:
            logger.error(f"Error loading image models: {e}")
            self.model_loaded = False
            self.nsfw_detector = None
            self.violence_detector = None
            self.result_cache = {}

    
    
    def _hash_image(self, image):
        """Generate hash for image to use as cache key"""
        try:
            # Convert image to bytes for hashing
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_bytes = img_byte_arr.getvalue()
            
            # Generate MD5 hash
            return hashlib.md5(img_bytes).hexdigest()
        except Exception as e:
            logger.error(f"Error hashing image: {e}")
            return None
    
    
    def analyze_file(self, image_file):
        """Analyze image file for unsafe content"""
        try:
            image = Image.open(image_file.stream)
            return self._analyze_image(image)
        except Exception as e:
            logger.error(f"Error analyzing image file: {e}")
            return self._error_response(str(e))
    
    
    def analyze_base64(self, image_base64):
        """Analyze base64 encoded image"""
        try:
            image_data = base64.b64decode(image_base64)
            image = Image.open(io.BytesIO(image_data))
            return self._analyze_image(image)
        except Exception as e:
            logger.error(f"Error analyzing base64 image: {e}")
            return self._error_response(str(e))
    
    
    def _analyze_image(self, image):
        """Internal method to analyze PIL Image object"""
        try:
            import time
            start_time = time.time()
            
            # Convert to RGB if needed
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize image if too large (improves performance significantly)
            max_size = 1024
            if image.width > max_size or image.height > max_size:
                logger.info(f"Resizing image from {image.width}x{image.height}")
                image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
                logger.info(f"Resized to {image.width}x{image.height}")
            
            # Check cache first
            image_hash = self._hash_image(image)
            if image_hash and image_hash in self.result_cache:
                logger.info(f"Cache hit! Returning cached result for image {image_hash[:8]}...")
                cached_result = self.result_cache[image_hash].copy()
                cached_result['from_cache'] = True
                cached_result['processing_time'] = time.time() - start_time
                return cached_result
            
            # Run NSFW detection (always available)
            nsfw_predictions = self.nsfw_detector(image)
            
            # Run violence detection only if model loaded
            if self.violence_detector is not None:
                violence_predictions = self.violence_detector(image)
            else:
                violence_predictions = [{"label": "non-violence", "score": 1.0}]
            
            processing_time = time.time() - start_time
            logger.info(f"Image analysis completed in {processing_time:.2f} seconds")
            
            # Parse NSFW predictions
            nsfw_score = 0.0
            normal_score = 0.0
            
            for pred in nsfw_predictions:
                if pred['label'] == 'nsfw':
                    nsfw_score = pred['score']
                elif pred['label'] == 'normal':
                    normal_score = pred['score']
            
            # Parse violence predictions
            violence_score = 0.0
            non_violence_score = 0.0
            
            logger.info(f"Violence predictions: {violence_predictions}")
            
            for pred in violence_predictions:
                label = pred['label']
                # LABEL_1 is violence, LABEL_0 is non-violence
                # Also check for explicit text labels in case model config changes
                is_violence = (label == 'LABEL_1' or 
                              'violence' in label.lower() or 
                              'violent' in label.lower())
                
                if is_violence:
                    violence_score = pred['score']
                else:
                    non_violence_score = pred['score']
            
            logger.info(f"Violence score: {violence_score:.3f}, Non-violence score: {non_violence_score:.3f}")
            logger.info(f"NSFW score: {nsfw_score:.3f}, Normal score: {normal_score:.3f}")
            
            # Apply smart filtering for violence false positives
            # If violence is detected but NSFW is very low, it's likely a false positive
            # This prevents nature images, sports, etc. from being flagged as violent
            adjusted_violence_score = violence_score
            
            # Only apply aggressive filtering for very obvious false positives
            # Be more conservative to avoid missing actual injuries/violence
            if violence_score > 0.6 and nsfw_score < 0.10 and normal_score > 0.85:
                # Very high violence, very low NSFW, and very high normal confidence
                # This pattern suggests nature/sports false positive
                adjusted_violence_score = violence_score * 0.4
                logger.info(f"Applied false positive filter: violence reduced from {violence_score:.3f} to {adjusted_violence_score:.3f}")
            elif violence_score > 0.5 and nsfw_score < 0.05 and normal_score > 0.90:
                # Extremely obvious false positive (e.g., pure nature scenes)
                adjusted_violence_score = violence_score * 0.5
                logger.info(f"Applied weak false positive filter: violence reduced to {adjusted_violence_score:.3f}")
            
            # Determine overall safety using adjusted scores
            max_threat_score = max(nsfw_score, adjusted_violence_score)
            # Stricter threshold - even minor threats should not be marked as completely safe
            is_safe = max_threat_score < 0.20  # Lowered to 20% to catch injuries/mild violence
            
            # Construct categories dict with adjusted violence
            categories = {
                "nsfw": float(nsfw_score),
                "violence": float(adjusted_violence_score),  # Use adjusted score
                "safe": float(max(normal_score, 1.0 - max_threat_score))  # Take max of model's normal confidence
            }
            
            # Overall score is the maximum threat
            overall_score = max_threat_score
            
            if is_safe:
                threat_level = "safe"
            elif overall_score > 0.6:  # High threat
                threat_level = "high"
            elif overall_score > 0.30:  # Medium threat (includes injuries ~20-30%)
                threat_level = "medium"
            else:
                threat_level = "low"  # 20-30% range
            
            result = {
                "is_safe": is_safe,
                "threat_level": threat_level,
                "categories": categories,
                "overall_score": round(overall_score, 3),
                "processing_time": round(processing_time, 3),
                "from_cache": False,
                "image_info": {
                    "width": image.width,
                    "height": image.height,
                    "mode": image.mode
                },
                "models": {
                    "nsfw": "Falconsai/nsfw_image_detection",
                    "violence": "jaranohaal/vit-base-violence-detection"
                }
            }
            
            # Store in cache (implement simple LRU by clearing oldest if full)
            if image_hash:
                if len(self.result_cache) >= self.cache_max_size:
                    # Remove oldest entry (simple FIFO strategy)
                    oldest_key = next(iter(self.result_cache))
                    del self.result_cache[oldest_key]
                    logger.info(f"Cache full, removed oldest entry")
                
                self.result_cache[image_hash] = result.copy()
                logger.info(f"Cached result for image {image_hash[:8]}... (cache size: {len(self.result_cache)})")
            
            return result
            
        except Exception as e:
            logger.error(f"Error in image analysis: {e}")
            return self._error_response(str(e))
    
    
    def _error_response(self, error_msg):
        """Generate error response"""
        return {
            "is_safe": True,
            "threat_level": "safe",
            "categories": {
                "nsfw": 0.0,
                "violence": 0.0
            },
            "overall_score": 0.0,
            "error": error_msg
        }


# Instructions for implementing actual NSFW detection:
"""
OPTION 1: Using NudeNet (Recommended)
--------------------------------------
Install: pip install nudenet

from nudenet import NudeDetector
detector = NudeDetector()

# In _analyze_image:
predictions = detector.detect('image.jpg')
# Parse predictions for NSFW content


OPTION 2: Using Hugging Face Vision Models
-------------------------------------------
from transformers import pipeline

detector = pipeline("image-classification", 
                   model="Falconsai/nsfw_image_detection")

# In _analyze_image:
predictions = detector(image)


OPTION 3: Using External API (Clarifai, AWS Rekognition)
--------------------------------------------------------
import clarifai

# Call API with image
# Parse response for NSFW scores
"""
