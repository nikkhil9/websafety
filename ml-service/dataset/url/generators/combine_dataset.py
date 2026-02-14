"""
Combine all URL datasets and create train/val/test splits
"""
import json
import random
from collections import Counter

def load_jsonl(filepath):
    """Load JSONL file"""
    data = []
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data

def save_jsonl(data, filepath):
    """Save to JSONL file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')

def combine_and_split():
    """Combine all URL datasets and create splits"""
    print("📦 Combining URL datasets...")
    
    # Load all datasets
    safe_urls = load_jsonl("../raw/safe_urls.jsonl")
    phishing_urls = load_jsonl("../raw/phishing_urls.jsonl")
    malware_urls = load_jsonl("../raw/malware_urls.jsonl")
    spam_urls = load_jsonl("../raw/spam_urls.jsonl")
    suspicious_urls = load_jsonl("../raw/suspicious_urls.jsonl")
    
    # Combine
    all_urls = safe_urls + phishing_urls + malware_urls + spam_urls + suspicious_urls
    
    print(f"✅ Total URLs: {len(all_urls)}")
    print(f"   Category breakdown:")
    labels = [url['label'] for url in all_urls]
    for label, count in Counter(labels).items():
        print(f"   - {label}: {count}")
    
    # Shuffle
    random.shuffle(all_urls)
    
    # Split: 70% train, 15% val, 15% test
    train_size = int(0.7 * len(all_urls))
    val_size = int(0.15 * len(all_urls))
    
    train_data = all_urls[:train_size]
    val_data = all_urls[train_size:train_size + val_size]
    test_data = all_urls[train_size + val_size:]
    
    print(f"\n📊 Split sizes:")
    print(f"   - Train: {len(train_data)} (70%)")
    print(f"   - Val: {len(val_data)} (15%)")
    print(f"   - Test: {len(test_data)} (15%)")
    
    # Save splits
    save_jsonl(train_data, "../processed/train_urls.jsonl")
    save_jsonl(val_data, "../processed/val_urls.jsonl")
    save_jsonl(test_data, "../processed/test_urls.jsonl")
    
    # Save combined
    save_jsonl(all_urls, "../raw/websafety_urls_9k.jsonl")
    
    print(f"\n💾 Saved to:")
    print(f"   - ../raw/websafety_urls_9k.jsonl (combined)")
    print(f"   - ../processed/train_urls.jsonl")
    print(f"   - ../processed/val_urls.jsonl")
    print(f"   - ../processed/test_urls.jsonl")
    
    return {
        "total": len(all_urls),
        "train": len(train_data),
        "val": len(val_data),
        "test": len(test_data),
        "categories": dict(Counter(labels))
    }

if __name__ == "__main__":
    stats = combine_and_split()
    print(f"\n✅ Dataset generation complete!")
    print(f"📈 Ready for feature extraction and model training")
