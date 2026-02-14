"""
Feature Extraction for URL Classification
Extracts 20 features from each URL for ML training
"""
import json
import re
from urllib.parse import urlparse
import math

# https://github.com/MarkEZhang/URLNet/blob/master/url_features.py
# URL shorteners list
URL_SHORTENERS = ['bit.ly', 'goo.gl', 'tinyurl.com', 't.co', 'ow.ly', 'is.gd', 'buff.ly', 'adf.ly']

# Suspicious TLDs
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.online', '.download']

# Suspicious keywords
SUSPICIOUS_KEYWORDS = [
    'login', 'verify', 'account', 'secure', 'update', 'confirm',
    'banking', 'paypal', 'ebay', 'amazon', 'suspended', 'limited'
]

def calculate_entropy(text):
    """Calculate Shannon entropy of a string"""
    if not text:
        return 0.0
    
    prob = [float(text.count(c)) / len(text) for c in dict.fromkeys(list(text))]
    entropy = - sum([p * math.log(p) / math.log(2.0) for p in prob])
    return entropy

def extract_url_features(url):
    """
    Extract 20 features from URL
    
    Returns:
        dict: Feature vector
    """
    try:
        parsed = urlparse(url)
        domain = parsed.netloc.lower()
        path = parsed.path.lower()
        full_url = url.lower()
        
        # Feature 1: URL Length
        url_length = len(url)
        
        # Feature 2: Domain Length
        domain_length = len(domain)
        
        # Feature 3: Path Length
        path_length = len(path)
        
        # Feature 4: Number of subdomains
        subdomain_count = domain.count('.')
        
        # Feature 5: Has HTTPS
        has_https = 1 if parsed.scheme == 'https' else 0
        
        # Feature 6: Has IP address
        ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
        has_ip = 1 if ip_pattern.match(domain) else 0
        
        # Feature 7: Suspicious TLD
        suspicious_tld = 1 if any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS) else 0
        
        # Feature 8: Special character count
        special_chars = ['@', '-', '_', '%', '&', '=', '?', '#']
        special_char_count = sum(url.count(char) for char in special_chars)
        
        # Feature 9: Digit count
        digit_count = sum(c.isdigit() for c in url)
        
        # Feature 10: Is URL shortener
        is_shortener = 1 if any(shortener in domain for shortener in URL_SHORTENERS) else 0
        
        # Feature 11: Has suspicious keywords
        has_suspicious_keywords = 1 if any(keyword in full_url for keyword in SUSPICIOUS_KEYWORDS) else 0
        
        # Feature 12: Domain entropy
        domain_entropy = calculate_entropy(domain)
        
        # Feature 13: Path entropy
        path_entropy = calculate_entropy(path) if path else 0.0
        
        # Feature 14: Number of dots in domain
        dot_count = domain.count('.')
        
        # Feature 15: Number of hyphens in domain
        hyphen_count = domain.count('-')
        
        # Feature 16: Has port number
        has_port = 1 if ':' in domain else 0
        
        # Feature 17: Query parameter count
        query_param_count = parsed.query.count('&') + (1 if parsed.query else 0)
        
        # Feature 18: Has double slashes in path
        has_double_slash = 1 if '//' in path else 0
        
        # Feature 19: Ratio of digits to total length
        digit_ratio = digit_count / url_length if url_length > 0 else 0
        
        # Feature 20: Ratio of special chars to total length
        special_char_ratio = special_char_count / url_length if url_length > 0 else 0
        
        return {
            "url_length": url_length,
            "domain_length": domain_length,
            "path_length": path_length,
            "subdomain_count": subdomain_count,
            "has_https": has_https,
            "has_ip": has_ip,
            "suspicious_tld": suspicious_tld,
            "special_char_count": special_char_count,
            "digit_count": digit_count,
            "is_shortener": is_shortener,
            "has_suspicious_keywords": has_suspicious_keywords,
            "domain_entropy": round(domain_entropy, 4),
            "path_entropy": round(path_entropy, 4),
            "dot_count": dot_count,
            "hyphen_count": hyphen_count,
            "has_port": has_port,
            "query_param_count": query_param_count,
            "has_double_slash": has_double_slash,
            "digit_ratio": round(digit_ratio, 4),
            "special_char_ratio": round(special_char_ratio, 4)
        }
    
    except Exception as e:
        print(f"Error extracting features from {url}: {e}")
        return None

def extract_features_from_dataset(input_file, output_file):
    """Extract features from dataset and save"""
    print(f"📊 Extracting features from {input_file}...")
    
    data = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            item = json.loads(line)
            features = extract_url_features(item['url'])
            
            if features:
                data.append({
                    "url": item['url'],
                    "label": item['label'],
                    "features": features
                })
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')
    
    print(f"✅ Extracted features for {len(data)} URLs")
    print(f"💾 Saved to {output_file}")
    
    return data

if __name__ == "__main__":
    # Extract features for all splits
    extract_features_from_dataset(
        "processed/train_urls.jsonl",
        "processed/train_urls_features.jsonl"
    )
    
    extract_features_from_dataset(
        "processed/val_urls.jsonl",
        "processed/val_urls_features.jsonl"
    )
    
    extract_features_from_dataset(
        "processed/test_urls.jsonl",
        "processed/test_urls_features.jsonl"
    )
    
    print("\n✅ Feature extraction complete!")
