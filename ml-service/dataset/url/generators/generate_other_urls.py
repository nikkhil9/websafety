"""
Generate Malware, Spam, and Suspicious URL samples
- Malware: 1,500 URLs
- Spam: 1,000 URLs  
- Suspicious: 1,000 URLs
Total: 3,500 URLs
"""
import json
import random
from datetime import datetime

# Malware-related patterns
MALWARE_KEYWORDS = [
    "download", "free", "crack", "keygen", "patch", "serial",
    "torrent", "warez", "nulled", "activator", "loader"
]

SOFTWARE_NAMES = [
    "photoshop", "windows", "office", "antivirus", "game",
    "vpn", "software", "tool", "app", "program"
]

# Spam keywords
SPAM_KEYWORDS = [
    "win", "prize", "free", "gift", "offer", "deal", "discount",
    "click", "here", "limited", "now", "today", "urgent", "congratulations"
]

# Suspicious patterns
URL_SHORTENERS = ["bit.ly", "goo.gl", "tinyurl.com", "t.co", "ow.ly", "is.gd"]

def generate_malware_urls(count=1500):
    """Generate malware distribution URLs"""
    urls = []
    
    for _ in range(count):
        pattern_type = random.choice(['download', 'crack', 'ip_based'])
        
        if pattern_type == 'download':
            software = random.choice(SOFTWARE_NAMES)
            keyword = random.choice(MALWARE_KEYWORDS)
            tld = random.choice(['.top', '.xyz', '.download', '.ml', '.tk'])
            domain = f"{keyword}-{software}"
            url = f"http://{domain}{tld}/download.exe"
            
        elif pattern_type == 'crack':
            software = random.choice(SOFTWARE_NAMES)
            year = random.choice(['2023', '2024', '2025'])
            tld = random.choice(['.xyz', '.top', '.work'])
            url = f"http://crack-{software}-{year}{tld}/setup.exe"
            
        else:  # ip_based
            ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
            file = random.choice(['malware.exe', 'trojan.exe', 'virus.exe', 'backdoor.exe'])
            url = f"http://{ip}/{file}"
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "malware",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": pattern_type,
                "timestamp": datetime.now().isoformat()
            }
        })
    
    return urls

def generate_spam_urls(count=1000):
    """Generate spam/advertising URLs"""
    urls = []
    
    for _ in range(count):
        # Create spammy domain
        keywords = random.sample(SPAM_KEYWORDS, k=random.randint(2, 4))
        domain = "-".join(keywords)
        tld = random.choice(['.ga', '.cf', '.gq', '.tk', '.ml', '.xyz'])
        
        path_options = [
            "",
            "/click",
            "/offer",
            "/promo",
            f"/ref{random.randint(1000,9999)}"
        ]
        
        path = random.choice(path_options)
        url = f"http://{domain}{tld}{path}"
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "spam",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": "spam_advertising",
                "timestamp": datetime.now().isoformat()
            }
        })
    
    return urls

def generate_suspicious_urls(count=1000):
    """Generate suspicious URLs (shorteners, long URLs, etc.)"""
    urls = []
    
    for _ in range(count):
        pattern_type = random.choice(['shortener', 'very_long', 'many_subdomains', 'weird_chars'])
        
        if pattern_type == 'shortener':
            shortener = random.choice(URL_SHORTENERS)
            code = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(5, 8)))
            url = f"https://{shortener}/{code}"
            
        elif pattern_type == 'very_long':
            base = random.choice(['example.com', 'site.com', 'page.net'])
            long_path = '/'.join(['path' + str(i) for i in range(random.randint(10, 20))])
            url = f"https://{base}/{long_path}?param=" + 'x' * random.randint(50, 100)
            
        elif pattern_type == 'many_subdomains':
            subdomains = '.'.join([f'sub{i}' for i in range(random.randint(4, 8))])
            url = f"https://{subdomains}.example.com"
            
        else:  # weird_chars
            domain = 'site-' + '-'.join([str(random.randint(0, 9)) for _ in range(10)])
            url = f"http://{domain}.xyz?param=" + '&'.join([f"x{i}=val{i}" for i in range(10)])
        
        features = extract_features(url)
        
        urls.append({
            "url": url,
            "label": "suspicious",
            "features": features,
            "metadata": {
                "generated": True,
                "pattern": pattern_type,
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
    
    # Check for IP address
    import re
    ip_pattern = re.compile(r'^(\d{1,3}\.){3}\d{1,3}$')
    has_ip = bool(ip_pattern.match(domain))
    
    # Suspicious TLDs
    suspicious_tlds = ['.tk', '.ml', '.ga', '.cf', '.gq', '.xyz', '.top', '.work']
    has_suspicious_tld = any(domain.endswith(tld) for tld in suspicious_tlds)
    
    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "has_https": parsed.scheme == 'https',
        "has_ip": has_ip,
        "subdomain_count": domain.count('.'),
        "special_char_count": sum(url.count(c) for c in ['@', '-', '_', '%', '&', '=', '?']),
        "digit_count": sum(c.isdigit() for c in url),
        "suspicious_tld": has_suspicious_tld
    }

if __name__ == "__main__":
    print("⚠️ Generating Malware, Spam, and Suspicious URLs...")
    
    # Generate all types
    malware_urls = generate_malware_urls(1500)
    spam_urls = generate_spam_urls(1000)
    suspicious_urls = generate_suspicious_urls(1000)
    
    print(f"✅ Generated URLs:")
    print(f"   - Malware: {len(malware_urls)}")
    print(f"   - Spam: {len(spam_urls)}")
    print(f"   - Suspicious: {len(suspicious_urls)}")
    print(f"   Total: {len(malware_urls) + len(spam_urls) + len(suspicious_urls)}")
    
    # Save to separate files
    with open("../raw/malware_urls.jsonl", 'w', encoding='utf-8') as f:
        for url_data in malware_urls:
            f.write(json.dumps(url_data) + '\n')
    
    with open("../raw/spam_urls.jsonl", 'w', encoding='utf-8') as f:
        for url_data in spam_urls:
            f.write(json.dumps(url_data) + '\n')
    
    with open("../raw/suspicious_urls.jsonl", 'w', encoding='utf-8') as f:
        for url_data in suspicious_urls:
            f.write(json.dumps(url_data) + '\n')
    
    print(f"💾 Saved to ../raw/")
    print(f"📊 Sample malware: {malware_urls[0]['url']}")
    print(f"📊 Sample spam: {spam_urls[0]['url']}")
    print(f"📊 Sample suspicious: {suspicious_urls[0]['url']}")
