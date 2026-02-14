"""
Dataset Splitter - Creates train/validation/test splits
Splits 9K dataset into 70% train, 15% validation, 15% test
"""

import json
import random
from pathlib import Path
from collections import defaultdict

def load_dataset(file_path):
    """Load JSONL dataset"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def stratified_split(samples, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """
    Stratified split ensuring balanced distribution across:
    - Languages
    - Categories
    """
    # Group by (language, category)
    groups = defaultdict(list)
    for sample in samples:
        key = (sample['language'], sample['primary_label'])
        groups[key].append(sample)
    
    train, val, test = [], [], []
    
    # Split each group proportionally
    for key, group_samples in groups.items():
        random.shuffle(group_samples)
        n = len(group_samples)
        
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)
        
        train.extend(group_samples[:train_end])
        val.extend(group_samples[train_end:val_end])
        test.extend(group_samples[val_end:])
    
    # Shuffle final sets
    random.shuffle(train)
    random.shuffle(val)
    random.shuffle(test)
    
    return train, val, test

def save_jsonl(samples, file_path):
    """Save to JSONL"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')

def print_stats(name, samples):
    """Print statistics for a split"""
    total = len(samples)
    langs = defaultdict(int)
    cats = defaultdict(int)
    
    for s in samples:
        langs[s['language']] += 1
        cats[s['primary_label']] += 1
    
    print(f"\n{name}: {total} samples")
    print("  Languages:", {k: v for k, v in sorted(langs.items())})
    print("  Categories:", {k: v for k, v in sorted(cats.items())})

def split_dataset():
    """Main splitting function"""
    print("🔀 Splitting 9K dataset into train/val/test")
    
    # Paths
    base = Path(__file__).parent.parent
    input_file = base / "raw" / "websafety_9k_multilingual.jsonl"
    output_dir = base / "processed"
    output_dir.mkdir(exist_ok=True)
    
    # Load
    print(f"\n📂 Loading from: {input_file}")
    samples = load_dataset(input_file)
    print(f"   Total samples: {len(samples):,}")
    
    # Set seed for reproducibility
    random.seed(42)
    
    # Split
    print("\n✂️  Splitting with stratification...")
    train, val, test = stratified_split(samples)
    
    # Stats
    print_stats("Training", train)
    print_stats("Validation", val)
    print_stats("Test", test)
    
    # Save
    print("\n💾 Saving splits...")
    save_jsonl(train, output_dir / "train_9k.jsonl")
    save_jsonl(val, output_dir / "validation_9k.jsonl")
    save_jsonl(test, output_dir / "test_9k.jsonl")
    
    print(f"\n✅ Splits saved to: {output_dir}")
    print(f"   - train_9k.jsonl: {len(train):,} samples")
    print(f"   - validation_9k.jsonl: {len(val):,} samples")
    print(f"   - test_9k.jsonl: {len(test):,} samples")
    print("\n✨ Dataset ready for training!")

if __name__ == "__main__":
    split_dataset()
