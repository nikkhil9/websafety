"""
Model Evaluation Script for Web Safety Project
Demonstrates accuracy, precision, recall, and F1-score for faculty presentation
"""

import requests
import json
import time
from collections import defaultdict

# Configuration
BASE_URL = "http://localhost:5001"

# Test dataset with known labels
# These are manually labeled examples for evaluation
TEXT_TEST_DATA = [
    # Safe examples (label: 0)
    {"text": "Hello! Have a great day!", "label": 0, "category": "safe"},
    {"text": "Thank you for your help!", "label": 0, "category": "safe"},
    {"text": "This is a wonderful product", "label": 0, "category": "safe"},
    {"text": "I love learning new things", "label": 0, "category": "safe"},
    {"text": "Great work on the project", "label": 0, "category": "safe"},
    {"text": "The weather is nice today", "label": 0, "category": "safe"},
    {"text": "Can you help me with this?", "label": 0, "category": "safe"},
    {"text": "I appreciate your time", "label": 0, "category": "safe"},
    {"text": "This looks interesting", "label": 0, "category": "safe"},
    {"text": "Have a wonderful weekend", "label": 0, "category": "safe"},
    
    # Toxic examples (label: 1)
    {"text": "You are stupid and worthless", "label": 1, "category": "toxic"},
    {"text": "I hate you so much", "label": 1, "category": "toxic"},
    {"text": "You're an idiot", "label": 1, "category": "toxic"},
    {"text": "Go away, nobody likes you", "label": 1, "category": "toxic"},
    {"text": "You suck at everything", "label": 1, "category": "toxic"},
    {"text": "You're disgusting", "label": 1, "category": "toxic"},
    {"text": "I hope you fail", "label": 1, "category": "toxic"},
    {"text": "You're pathetic and dumb", "label": 1, "category": "toxic"},
    {"text": "Nobody wants you here", "label": 1, "category": "toxic"},
    {"text": "You're trash", "label": 1, "category": "toxic"},
    
    # Threatening examples (label: 1)
    {"text": "I will hurt you", "label": 1, "category": "threat"},
    {"text": "You better watch out", "label": 1, "category": "threat"},
    {"text": "I know where you live", "label": 1, "category": "threat"},
    {"text": "I'll make you pay for this", "label": 1, "category": "threat"},
    {"text": "You're going to regret this", "label": 1, "category": "threat"},
]

URL_TEST_DATA = [
    # Safe URLs (label: 0)
    {"url": "https://www.google.com", "label": 0, "category": "safe"},
    {"url": "https://github.com", "label": 0, "category": "safe"},
    {"url": "https://stackoverflow.com", "label": 0, "category": "safe"},
    {"url": "https://www.wikipedia.org", "label": 0, "category": "safe"},
    {"url": "https://www.youtube.com", "label": 0, "category": "safe"},
    
    # Malicious URLs (label: 1)
    {"url": "http://login-verify-account.tk", "label": 1, "category": "phishing"},
    {"url": "http://192.168.1.1/admin.php", "label": 1, "category": "suspicious"},
    {"url": "http://paypal-security-update.com/verify", "label": 1, "category": "phishing"},
    {"url": "http://free-download-virus.ml", "label": 1, "category": "malware"},
    {"url": "http://click-here-now.xyz/login", "label": 1, "category": "suspicious"},
]


def analyze_text(text):
    """Call text analysis API"""
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/text",
            json={"text": text},
            timeout=10
        )
        return response.json()
    except Exception as e:
        print(f"Error analyzing text: {e}")
        return None


def analyze_url(url):
    """Call URL analysis API"""
    try:
        response = requests.post(
            f"{BASE_URL}/analyze/url",
            json={"url": url},
            timeout=10
        )
        return response.json()
    except Exception as e:
        print(f"Error analyzing URL: {e}")
        return None


def evaluate_text_classifier():
    """Evaluate text classification model"""
    print("\n" + "="*70)
    print("  📝 TEXT CLASSIFICATION EVALUATION")
    print("="*70)
    
    predictions = []
    true_labels = []
    results = []
    
    for i, example in enumerate(TEXT_TEST_DATA, 1):
        print(f"\nTesting {i}/{len(TEXT_TEST_DATA)}: {example['category']}")
        print(f"Text: {example['text'][:50]}...")
        
        result = analyze_text(example['text'])
        if result:
            predicted = 0 if result['is_safe'] else 1
            predictions.append(predicted)
            true_labels.append(example['label'])
            
            results.append({
                'text': example['text'],
                'true_label': example['label'],
                'predicted': predicted,
                'threat_level': result['threat_level'],
                'score': result['overall_score'],
                'correct': predicted == example['label']
            })
            
            status = "✅ CORRECT" if predicted == example['label'] else "❌ WRONG"
            print(f"Predicted: {'Unsafe' if predicted else 'Safe'} (score: {result['overall_score']:.3f}) {status}")
        
        time.sleep(0.5)  # Avoid overwhelming API
    
    # Calculate metrics
    tp = sum(1 for i in range(len(predictions)) if predictions[i] == 1 and true_labels[i] == 1)
    tn = sum(1 for i in range(len(predictions)) if predictions[i] == 0 and true_labels[i] == 0)
    fp = sum(1 for i in range(len(predictions)) if predictions[i] == 1 and true_labels[i] == 0)
    fn = sum(1 for i in range(len(predictions)) if predictions[i] == 0 and true_labels[i] == 1)
    
    accuracy = (tp + tn) / len(predictions) if predictions else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Print results
    print("\n" + "="*70)
    print("  📊 TEXT CLASSIFICATION RESULTS")
    print("="*70)
    print(f"\n  Total Samples: {len(predictions)}")
    print(f"  Correct Predictions: {tp + tn}")
    print(f"  Wrong Predictions: {fp + fn}")
    print(f"\n  ✅ Accuracy:  {accuracy*100:.2f}%")
    print(f"  📍 Precision: {precision*100:.2f}%")
    print(f"  📍 Recall:    {recall*100:.2f}%")
    print(f"  📍 F1-Score:  {f1_score*100:.2f}%")
    print(f"\n  Confusion Matrix:")
    print(f"  ┌─────────────┬──────────┬──────────┐")
    print(f"  │   Actual ↓  │   Safe   │  Unsafe  │")
    print(f"  ├─────────────┼──────────┼──────────┤")
    print(f"  │ Safe        │   {tn:2d}     │   {fp:2d}     │")
    print(f"  │ Unsafe      │   {fn:2d}     │   {tp:2d}     │")
    print(f"  └─────────────┴──────────┴──────────┘")
    print("="*70)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'results': results,
        'confusion_matrix': {'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}
    }


def evaluate_url_classifier():
    """Evaluate URL classification model"""
    print("\n" + "="*70)
    print("  🔗 URL CLASSIFICATION EVALUATION")
    print("="*70)
    
    predictions = []
    true_labels = []
    results = []
    
    for i, example in enumerate(URL_TEST_DATA, 1):
        print(f"\nTesting {i}/{len(URL_TEST_DATA)}: {example['category']}")
        print(f"URL: {example['url']}")
        
        result = analyze_url(example['url'])
        if result:
            predicted = 0 if result['is_safe'] else 1
            predictions.append(predicted)
            true_labels.append(example['label'])
            
            results.append({
                'url': example['url'],
                'true_label': example['label'],
                'predicted': predicted,
                'threat_level': result['threat_level'],
                'score': result['overall_score'],
                'correct': predicted == example['label']
            })
            
            status = "✅ CORRECT" if predicted == example['label'] else "❌ WRONG"
            print(f"Predicted: {'Unsafe' if predicted else 'Safe'} (score: {result['overall_score']:.3f}) {status}")
        
        time.sleep(0.5)
    
    # Calculate metrics
    tp = sum(1 for i in range(len(predictions)) if predictions[i] == 1 and true_labels[i] == 1)
    tn = sum(1 for i in range(len(predictions)) if predictions[i] == 0 and true_labels[i] == 0)
    fp = sum(1 for i in range(len(predictions)) if predictions[i] == 1 and true_labels[i] == 0)
    fn = sum(1 for i in range(len(predictions)) if predictions[i] == 0 and true_labels[i] == 1)
    
    accuracy = (tp + tn) / len(predictions) if predictions else 0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    
    # Print results
    print("\n" + "="*70)
    print("  📊 URL CLASSIFICATION RESULTS")
    print("="*70)
    print(f"\n  Total Samples: {len(predictions)}")
    print(f"  Correct Predictions: {tp + tn}")
    print(f"  Wrong Predictions: {fp + fn}")
    print(f"\n  ✅ Accuracy:  {accuracy*100:.2f}%")
    print(f"  📍 Precision: {precision*100:.2f}%")
    print(f"  📍 Recall:    {recall*100:.2f}%")
    print(f"  📍 F1-Score:  {f1_score*100:.2f}%")
    print(f"\n  Confusion Matrix:")
    print(f"  ┌─────────────┬──────────┬──────────┐")
    print(f"  │   Actual ↓  │   Safe   │  Unsafe  │")
    print(f"  ├─────────────┼──────────┼──────────┤")
    print(f"  │ Safe        │   {tn:2d}     │   {fp:2d}     │")
    print(f"  │ Unsafe      │   {fn:2d}     │   {tp:2d}     │")
    print(f"  └─────────────┴──────────┴──────────┘")
    print("="*70)
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score,
        'results': results,
        'confusion_matrix': {'tp': tp, 'tn': tn, 'fp': fp, 'fn': fn}
    }


def save_results_to_file(text_results, url_results):
    """Save evaluation results to JSON file for reference"""
    results = {
        'text_classification': text_results,
        'url_classification': url_results,
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
    }
    
    with open('evaluation_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("\n✅ Results saved to: evaluation_results.json")


def main():
    """Run complete evaluation"""
    print("\n" + "="*70)
    print("  🧪 WEB SAFETY MODEL EVALUATION SUITE")
    print("  For Faculty Presentation & Project Defense")
    print("="*70)
    
    try:
        # Test connection
        response = requests.get(f"{BASE_URL}/")
        if response.status_code != 200:
            print("\n❌ ERROR: ML service not running!")
            print("   Please start the server: python app.py")
            return
        
        print("\n✅ ML Service is running\n")
        
        # Evaluate both classifiers
        text_results = evaluate_text_classifier()
        url_results = evaluate_url_classifier()
        
        # Save results
        save_results_to_file(text_results, url_results)
        
        # Final summary
        print("\n" + "="*70)
        print("  🎯 OVERALL SYSTEM PERFORMANCE SUMMARY")
        print("="*70)
        print(f"\n  Text Classification:")
        print(f"    • Accuracy:  {text_results['accuracy']*100:.2f}%")
        print(f"    • Precision: {text_results['precision']*100:.2f}%")
        print(f"    • Recall:    {text_results['recall']*100:.2f}%")
        print(f"    • F1-Score:  {text_results['f1_score']*100:.2f}%")
        
        print(f"\n  URL Classification:")
        print(f"    • Accuracy:  {url_results['accuracy']*100:.2f}%")
        print(f"    • Precision: {url_results['precision']*100:.2f}%")
        print(f"    • Recall:    {url_results['recall']*100:.2f}%")
        print(f"    • F1-Score:  {url_results['f1_score']*100:.2f}%")
        
        print("\n" + "="*70)
        print("  ✅ Evaluation Complete!")
        print("  📄 Results saved to: evaluation_results.json")
        print("  💡 Use these metrics in your project presentation")
        print("="*70 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to ML service")
        print("   Make sure the server is running on http://localhost:5001")
        print("   Run: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    main()
