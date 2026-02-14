"""
Generate Safe URL samples (3,000 URLs)
Based on legitimate, well-known websites
"""
import json
import random
from datetime import datetime

# Top legitimate domains
LEGITIMATE_DOMAINS = [
    # Tech & Social Media
    "google.com", "youtube.com", "facebook.com", "twitter.com", "instagram.com",
    "linkedin.com", "reddit.com", "pinterest.com", "tumblr.com", "tiktok.com",
    
    # E-commerce
    "amazon.com", "ebay.com", "etsy.com", "walmart.com", "target.com",
    "bestbuy.com", "alibaba.com", "shopify.com", "wayfair.com",
    
    # Tech Companies
    "microsoft.com", "apple.com", "github.com", "stackoverflow.com", "medium.com",
    "netflix.com", "spotify.com", "zoom.us", "adobe.com", "salesforce.com",
    
    # News & Media
    "cnn.com", "bbc.com", "nytimes.com", "theguardian.com", "forbes.com",
    "techcrunch.com", "reuters.com", "bloomberg.com", "wsj.com", "npr.org",
    
    # Education
    "wikipedia.org", "khanacademy.org", "coursera.org", "udemy.com", "edx.org",
    "mit.edu", "stanford.edu", "harvard.edu", "ox.ac.uk", "cambridge.org",
    
    # Government & Organizations
    "gov.uk", "usa.gov", "europa.eu", "un.org", "who.int",
    
    # Productivity & Tools
    "dropbox.com", "slack.com", "trello.com", "notion.so", "canva.com",
    "grammarly.com", "mailchimp.com", "wordpress.com", "blogger.com",
    
    # Entertainment
    "imdb.com", "twitch.tv", "soundcloud.com", "vimeo.com", "dailymotion.com"
]

# Common paths for legitimate sites
PATHS = [
    "/", "/about", "/contact", "/products", "/services", "/blog",
    "/news", "/support", "/help", "/faq", "/pricing", "/careers",
    "/team", "/privacy", "/terms", "/documentation", "/api",
    "/login", "/signup", "/account", "/dashboard", "/settings"
]

# Subdomains
SUBDOMAINS = ["www", "blog", "api", "shop", "store", "mail", "news", "support", "help", "docs"]

def generate_safe_urls(count=3000):
    """Generate safe URL samples"""
    urls = []
    used_urls = set()
    
    print(f"🔒 Generating {count} Safe URLs...")
    
    while len(urls) < count:
        domain = random.choice(LEGITIMATE_DOMAINS)
        
        # Variations
        variation = random.choice([
            'https_root',
            'http_root', 
            'https_path',
            'subdomain_https',
            'subdomain_path',
            'https_query'
        ])
        
        if variation == 'https_root':
            url = f"https://{domain}"
        elif variation == 'http_root':
            url = f"http://{domain}"
        elif variation == 'https_path':
            path = random.choice(PATHS)
            url = f"https://{domain}{path}"
        elif variation == 'subdomain_https':
            subdomain = random.choice(SUBDOMAINS)
            url = f"https://{subdomain}.{domain}"
        elif variation == 'subdomain_path':
            subdomain = random.choice(SUBDOMAINS)
            path = random.choice(PATHS)
            url = f"https://{subdomain}.{domain}{path}"
        elif variation == 'https_query':
            url = f"https://{domain}/search?q=python+tutorial"
        
        # Avoid duplicates
        if url not in used_urls:
            used_urls.add(url)
            
            # Extract features
            features = extract_features(url)
            
            urls.append({
                "url": url,
                "label": "safe",
                "features": features,
                "metadata": {
                    "generated": True,
                    "pattern": variation,
                    "timestamp": datetime.now().isoformat(),
                    "source": "legitimate_domains"
                }
            })
    
    print(f"✅ Generated {len(urls)} safe URLs")
    return urls

def extract_features(url):
    """Extract basic features from URL"""
    from urllib.parse import urlparse
    
    parsed = urlparse(url)
    domain = parsed.netloc
    path = parsed.path
    
    return {
        "url_length": len(url),
        "domain_length": len(domain),
        "path_length": len(path),
        "has_https": parsed.scheme == 'https',
        "subdomain_count": domain.count('.'),
        "special_char_count": sum(url.count(c) for c in ['@', '-', '_', '%', '&', '=', '?']),
        "digit_count": sum(c.isdigit() for c in url)
    }

if __name__ == "__main__":
    # Generate safe URLs
    safe_urls = generate_safe_urls(3000)
    
    # Save to file
    output_file = "../raw/safe_urls.jsonl"
    with open(output_file, 'w', encoding='utf-8') as f:
        for url_data in safe_urls:
            f.write(json.dumps(url_data) + '\n')
    
    print(f"💾 Saved to {output_file}")
    print(f"📊 Sample: {safe_urls[0]['url']}")
