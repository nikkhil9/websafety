"""
URL Collector for WebSafety Dataset

Collects URLs from various public sources:
- PhishTank for phishing URLs
- URLhaus for malware URLs
- Common safe URLs from curated lists

Usage:
    python -m dataset.collectors.url_collector --output dataset/raw/urls/
"""

import json
import os
import argparse
from datetime import datetime
from typing import List, Dict
import random
import time

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests


class URLCollector:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'WebSafety-Research-Dataset/1.0'
        })
    
    def collect_phishing_urls(self, limit: int = 1000) -> List[Dict]:
        """
        Collect phishing URLs from PhishTank API
        Note: PhishTank requires API key for full access
        """
        print(f"Collecting up to {limit} phishing URLs from PhishTank...")
        urls = []
        
        try:
            # PhishTank provides a JSON dump
            # For demo purposes, we'll use recent phishing patterns
            # In production, download from: http://data.phishtank.com/data/online-valid.json
            
            phishing_patterns = [
                ("http://paypa1-verify.tk/login", "PayPal phishing"),
                ("http://amazon-account-locked.ml/verify", "Amazon phishing"),
                ("http://appleid-unlock.cf/login", "Apple ID phishing"),
                ("http://secure-banking.ga/login", "Banking phishing"),
                ("http://netflix-payment.tk/update", "Netflix phishing"),
                ("http://microsoft-security.ml/alert", "Microsoft phishing"),
                ("http://facebook-security.cf/verify", "Facebook phishing"),
                ("http://instagram-verify.tk/account", "Instagram phishing"),
                ("http://google-accountrecovery.ml/", "Google phishing"),
                ("http://crypto-wallet-verify.tk/", "Crypto phishing"),
            ]
            
            for idx, (url, description) in enumerate(phishing_patterns[:limit]):
                urls.append({
                    "id": f"WS-{str(idx+1).zfill(8)}",
                    "text": f"Suspicious link: {url}",
                    "url": url,
                    "primary_label": "phishing",
                    "secondary_labels": ["scam"],
                    "severity": "high",
                    "context": "email",
                    "language": "en",
                    "target_demographic": "adults",
                    "contains_pii": False,
                    "requires_context": False,
                    "is_sarcasm": False,
                    "is_borderline": False,
                    "cultural_context": "global",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source": "phishtank_simulated",
                    "notes": description
                })
            
            print(f"✓ Collected {len(urls)} phishing URLs")
            
        except Exception as e:
            print(f"✗ Error collecting phishing URLs: {e}")
        
        return urls
    
    def collect_malware_urls(self, limit: int = 500) -> List[Dict]:
        """
        Collect malware URLs
        Note: URLhaus API can be used for real data
        """
        print(f"Collecting up to {limit} malware URLs...")
        urls = []
        
        try:
            # URLhaus patterns (simulated for safety)
            malware_patterns = [
                ("http://download-free-software.tk/setup.exe", "Malware installer"),
                ("http://codec-required.ml/player.exe", "Fake codec"),
                ("http://security-update.ga/update.exe", "Fake update"),
                ("http://free-antivirus.tk/scan.exe", "Fake antivirus"),
                ("http://crack-download.ml/keygen.exe", "Crack malware"),
            ]
            
            for idx, (url, description) in enumerate(malware_patterns[:limit]):
                urls.append({
                    "id": f"WS-{str(len(urls)+10000).zfill(8)}",
                    "text": f"Download link: {url}",
                    "url": url,
                    "primary_label": "malware",
                    "secondary_labels": ["scam"],
                    "severity": "high",
                    "context": "other",
                    "language": "en",
                    "target_demographic": "all",
                    "contains_pii": False,
                    "requires_context": False,
                    "is_sarcasm": False,
                    "is_borderline": False,
                    "cultural_context": "global",
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "source": "urlhaus_simulated",
                    "notes": description
                })
            
            print(f"✓ Collected {len(urls)} malware URLs")
            
        except Exception as e:
            print(f"✗ Error collecting malware URLs: {e}")
        
        return urls
    
    def collect_safe_urls(self, limit: int = 1000) -> List[Dict]:
        """
        Collect known safe URLs from curated list
        """
        print(f"Collecting up to {limit} safe URLs...")
        urls = []
        
        safe_urls = [
            ("https://www.wikipedia.org", "Wikipedia - general knowledge"),
            ("https://www.github.com", "GitHub - code repository"),
            ("https://www.stackoverflow.com", "Stack Overflow - Q&A"),
            ("https://www.youtube.com", "YouTube - video platform"),
            ("https://www.amazon.com", "Amazon - e-commerce"),
            ("https://www.google.com", "Google - search engine"),
            ("https://www.reddit.com", "Reddit - discussion forum"),
            ("https://www.twitter.com", "Twitter - social media"),
            ("https://www.linkedin.com", "LinkedIn - professional network"),
            ("https://www.netflix.com", "Netflix - streaming"),
            ("https://www.bbc.com/news", "BBC News"),
            ("https://www.nytimes.com", "New York Times"),
            ("https://www.medium.com", "Medium - blogging"),
            ("https://www.instagram.com", "Instagram - social media"),
            ("https://www.facebook.com", "Facebook - social network"),
        ]
        
        for idx, (url, description) in enumerate(safe_urls[:limit]):
            urls.append({
                "id": f"WS-{str(len(urls)+20000).zfill(8)}",
                "text": f"Check out this link: {url}",
                "url": url,
                "primary_label": "safe",
                "secondary_labels": [],
                "severity": "low",
                "context": "social_media",
                "language": "en",
                "target_demographic": "all",
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "global",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "curated_safe",
                "notes": description
            })
        
        print(f"✓ Collected {len(urls)} safe URLs")
        return urls
    
    def save_urls(self, urls: List[Dict], filename: str):
        """Save URLs to JSONL file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            for url_data in urls:
                f.write(json.dumps(url_data, ensure_ascii=False) + '\n')
        print(f"✓ Saved {len(urls)} URLs to {filepath}")
    
    def collect_all(self, phishing_limit=1000, malware_limit=500, safe_limit=1000):
        """Collect all URL types"""
        print("=" * 60)
        print("WebSafety URL Collector")
        print("=" * 60)
        
        # Collect phishing URLs
        phishing_urls = self.collect_phishing_urls(phishing_limit)
        self.save_urls(phishing_urls, "phishing_urls.jsonl")
        
        time.sleep(1)  # Rate limiting
        
        # Collect malware URLs
        malware_urls = self.collect_malware_urls(malware_limit)
        self.save_urls(malware_urls, "malware_urls.jsonl")
        
        time.sleep(1)
        
        # Collect safe URLs
        safe_urls = self.collect_safe_urls(safe_limit)
        self.save_urls(safe_urls, "safe_urls.jsonl")
        
        # Combine all
        all_urls = phishing_urls + malware_urls + safe_urls
        random.shuffle(all_urls)
        self.save_urls(all_urls, "all_urls.jsonl")
        
        print("\n" + "=" * 60)
        print("Collection Summary:")
        print(f"  Phishing: {len(phishing_urls)}")
        print(f"  Malware:  {len(malware_urls)}")
        print(f"  Safe:     {len(safe_urls)}")
        print(f"  Total:    {len(all_urls)}")
        print("=" * 60)
        print("\n📝 Note: This is simulated data for demonstration.")
        print("For production, integrate with real APIs:")
        print("  - PhishTank: http://www.phishtank.com/api_info.php")
        print("  - URLhaus: https://urlhaus-api.abuse.ch/")
        print("  - OpenPhish: https://openphish.com/")


def main():
    parser = argparse.ArgumentParser(
        description='Collect URLs for WebSafety Dataset'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dataset/raw/urls',
        help='Output directory for collected URLs'
    )
    parser.add_argument(
        '--phishing',
        type=int,
        default=1000,
        help='Number of phishing URLs to collect'
    )
    parser.add_argument(
        '--malware',
        type=int,
        default=500,
        help='Number of malware URLs to collect'
    )
    parser.add_argument(
        '--safe',
        type=int,
        default=1000,
        help='Number of safe URLs to collect'
    )
    
    args = parser.parse_args()
    
    collector = URLCollector(args.output)
    collector.collect_all(
        phishing_limit=args.phishing,
        malware_limit=args.malware,
        safe_limit=args.safe
    )


if __name__ == '__main__':
    main()
