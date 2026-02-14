"""
Generate Phishing URL samples (2,500 URLs)
Includes typosquatting, suspicious TLDs, and keyword stuffing patterns
"""
import json
import random
from datetime import datetime

# Major brands for typosquatting
BRANDS = [
    "paypal", "google", "facebook", "amazon", "microsoft", "apple",
    "netflix", "spotify", "instagram", "twitter", "linkedin", "ebay",
    "yahoo", "dropbox", "adobe", "whatsapp", "telegram", "github"
]

# Suspicious TLDs commonly used for phishing
SUSPICIOUS_TLDS = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click', '.online']

# Phishing keywords
PHISHING_KEYWORDS = [
    "login", "verify", "account", "secure", "update", "confirm",
    "banking", "suspended", "limited", "unusual", "urgent", "action",
    "required", "validate", "restore", "unlock", "blocked", "expires"
]

# Banking/financial terms
FINANCIAL_TERMS = [
    "bank", "payment", "paypal", "transaction", "transfer", "card",
    "visa", "mastercard", "wallet", "crypto", "bitcoin"
]

def generate_typosquatting_urls(count=800):
    """Generate typosquatting URLs"""
    urls = []
    
    typo_patterns = [
        lambda b: b.replace('o', '0'),  # google -> g00gle
        lambda b: b.replace('l', '1'),  # paypal -> paypa1
        lambda b: b.replace('e', '3'),  # facebook -> fac3book
        lambda b: b + 'online',         # amazon -> amazononline
        lambda b: 'secure-' + b,        # secure-paypal
        lambda b: b + '-login',         # netflix-login
        lambda b: b.replace('a', '4'),  # amazon -> 4mazon
        lambda b: b + b[random.choice([-2, -1])],  # paypal -> paypall
    ]
    
    for _ in range(count):
        brand = random.choice(BRANDS)
        pattern = random.choice(typo_patterns)
        typo_brand = pattern(brand)
        tld = random.choice(SUSPICIOUS_TLDS + ['.com', '.net'])
        
        # Variation
        if random.random() < 0.5:
            url = f"https://{typo_brand}{tld}"
        else:
            path = random.choice(["/login", "/verify", "/secure", "/account"])
            url = f"https://{typo_brand}{tld}{path}"
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "phishing",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": "typosquatting",
                "original_brand": brand,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    return urls

def generate_keyword_stuffing_urls(count=900):
    """Generate keyword-stuffed phishing URLs"""
    urls = []
    
    for _ in range(count):
        # Create keyword-stuffed domain
        keywords = random.sample(PHISHING_KEYWORDS, k=random.randint(3, 5))
        domain = "-".join(keywords)
        tld = random.choice(SUSPICIOUS_TLDS + ['.com', '.net', '.org'])
        
        if random.random() < 0.6:
            url = f"https://{domain}{tld}"
        else:
            path = random.choice(["/now", "/click", "/here", "/urgent"])
            url = f"https://{domain}{tld}{path}"
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "phishing",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": "keyword_stuffing",
                "keywords": keywords,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    return urls

def generate_financial_phishing_urls(count=800):
    """Generate financial/banking phishing URLs"""
    urls = []
    
    for _ in range(count):
        brand = random.choice(BRANDS)
        financial_term = random.choice(FINANCIAL_TERMS)
        keyword = random.choice(PHISHING_KEYWORDS)
        
        patterns = [
            f"{brand}-{keyword}",
            f"{financial_term}-{keyword}",
            f"{keyword}-{brand}",
            f"secure{brand}",
            f"{brand}{keyword}",
        ]
        
        domain = random.choice(patterns)
        tld = random.choice(SUSPICIOUS_TLDS)
        
        url = f"https://{domain}{tld}"
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "phishing",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": "financial_phishing",
                "timestamp": datetime.now().isoformat()
            }
        })
    
    return urls

def extract_features(url):
    """Extract basic features from URL"""
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    
    # Check for typosquatting indicators
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work', '.click']
    has_suspicious_tld = any(domain.endswith(tld) for tld in suspicious_tlds)
    
    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "has_https": parsed.scheme == 'https',
        "subdomain_count": domain.count('.'),
        "special_char_count": sum(url.count(c) for c in ['@', '-', '_', '%', '&', '=', '?']),
        "digit_count": sum(c.isdigit() for c in url),
        "suspicious_tld": has_suspicious_tld
    }

if __name__ == "__main__":
    print("🎣 Generating Phishing URLs...")
    
    # Generate different types
    typo_urls = generate_typosquatting_urls(800)
    keyword_urls = generate_keyword_stuffing_urls(900)
    financial_urls = generate_financial_phishing_urls(800)
    
    all_phishing = typo_urls + keyword_urls + financial_urls
    
    print(f"✅ Generated {len(all_phishing)} phishing URLs")
    print(f"   - Typosquatting: {len(typo_urls)}")
    print(f"   - Keyword stuffing: {len(keyword_urls)}")
    print(f"   - Financial phishing: {len(financial_urls)}")
    
    # Save to file
    output_file = "../raw/phishing_urls.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for url_data in all_phishing:
            f.write(json.dumps(url_data) + '\n')
    
    print(f"💾 Saved to {output_file}")
    print(f"📊 Sample typo: {typo_urls[0]['url']}")
    print(f"📊 Sample keyword: {keyword_urls[0]['url']}")
