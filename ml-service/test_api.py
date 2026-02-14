"""
Test script for Web Safety ML Service
Run this script to test all endpoints
"""

import requests
import json

# Configuration
BASE_URL = "http://localhost:5001"

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    print(f"Response:")
    print(json.dumps(response.json(), indent=2))
    print(f"{'='*60}\n")


def test_health_check():
    """Test health check endpoint"""
    print("\n🔍 Testing Health Check...")
    response = requests.get(f"{BASE_URL}/")
    print_response("Health Check", response)


def test_text_analysis():
    """Test text analysis endpoint"""
    print("\n📝 Testing Text Analysis...")
    
    test_cases = [
        {
            "name": "Safe Text",
            "text": "Hello! This is a friendly message. Have a great day!"
        },
        {
            "name": "Toxic Text",
            "text": "You are stupid and I hate you!"
        },
        {
            "name": "Threatening Text",
            "text": "I will hurt you if you don't do what I say"
        }
    ]
    
    for case in test_cases:
        print(f"\n  Testing: {case['name']}")
        print(f"  Text: {case['text']}")
        
        response = requests.post(
            f"{BASE_URL}/analyze/text",
            json={"text": case["text"]}
        )
        print_response(f"Text Analysis - {case['name']}", response)


def test_url_analysis():
    """Test URL analysis endpoint"""
    print("\n🔗 Testing URL Analysis...")
    
    test_cases = [
        {
            "name": "Safe URL (HTTPS)",
            "url": "https://www.google.com"
        },
        {
            "name": "Safe URL (GitHub)",
            "url": "https://github.com"
        },
        {
            "name": "Suspicious URL (No HTTPS)",
            "url": "http://example-login-verify-account.tk"
        },
        {
            "name": "Suspicious URL (IP Address)",
            "url": "http://192.168.1.100/login.php"
        },
        {
            "name": "Suspicious Keywords",
            "url": "https://paypal-security-update-verify.com/login"
        }
    ]
    
    for case in test_cases:
        print(f"\n  Testing: {case['name']}")
        print(f"  URL: {case['url']}")
        
        response = requests.post(
            f"{BASE_URL}/analyze/url",
            json={"url": case["url"]}
        )
        print_response(f"URL Analysis - {case['name']}", response)


def test_image_analysis():
    """Test image analysis endpoint (placeholder)"""
    print("\n🖼️  Testing Image Analysis...")
    print("\n  Note: Image analysis is using placeholder model")
    print("  To test with actual images, upload an image file\n")
    
    # For now, just show that endpoint exists
    # In real testing, you would upload an actual image file
    print("  Skipping image test (no sample image)")
    print("  To test manually, use tools like Postman or curl:")
    print("  curl -X POST -F 'image=@path/to/image.jpg' http://localhost:5001/analyze/image")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🧪 WEB SAFETY ML SERVICE - TEST SUITE")
    print("="*60)
    
    try:
        test_health_check()
        test_text_analysis()
        test_url_analysis()
        test_image_analysis()
        
        print("\n" + "="*60)
        print("  ✅ All tests completed!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to ML service")
        print("   Make sure the server is running on http://localhost:5001")
        print("   Run: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")


if __name__ == "__main__":
    run_all_tests()
