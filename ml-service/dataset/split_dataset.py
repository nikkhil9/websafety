"""
Split dataset into train/validation/test sets
"""
import json
import random
from collections import defaultdict
import os

def split_dataset(input_file, output_dir, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15):
    """Split dataset with stratification"""
    
    print("Loading dataset...")
    samples = []
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    
    print(f"Loaded {len(samples)} samples")
    
    # Group by label
    label_groups = defaultdict(list)
    for sample in samples:
        label = sample['primary_label']
        label_groups[label].append(sample)
    
    train_samples = []
    val_samples = []
    test_samples = []
    
    # Split each group
    for label, group in label_groups.items():
        random.shuffle(group)
        n = len(group)
        train_end = int(n * train_ratio)
        val_end = train_end + int(n * val_ratio)
        
        train_samples.extend(group[:train_end])
        val_samples.extend(group[train_end:val_end])
        test_samples.extend(group[val_end:])
    
    # Shuffle final splits
    random.shuffle(train_samples)
    random.shuffle(val_samples)
    random.shuffle(test_samples)
    
    # Save splits
    os.makedirs(output_dir, exist_ok=True)
    
    with open(f"{output_dir}/train.jsonl", 'w', encoding='utf-8') as f:
        for sample in train_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    with open(f"{output_dir}/validation.jsonl", 'w', encoding='utf-8') as f:
        for sample in val_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    with open(f"{output_dir}/test.jsonl", 'w', encoding='utf-8') as f:
        for sample in test_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"\n✓ Train: {len(train_samples)} samples")
    print(f"✓ Validation: {len(val_samples)} samples")
    print(f"✓ Test: {len(test_samples)} samples")
    print(f"\nFiles saved to: {output_dir}/")

if __name__ == "__main__":
    split_dataset(
        "dataset/processed/websafety_initial.jsonl",
        "dataset/processed"
    )
