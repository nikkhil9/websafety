"""
Data Splitter for WebSafety Dataset

Creates stratified train/validation/test splits.

Usage:
    python -m dataset.processing.splitter --input dataset/processed/balanced.jsonl --output dataset/processed/
"""

import json
import os
import argparse
from typing import List, Dict
from collections import defaultdict
import random


class DatasetSplitter:
    def __init__(self, train_ratio=0.7, val_ratio=0.15, test_ratio=0.15, random_seed=42):
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.random_seed = random_seed
        
        random.seed(random_seed)
    
    def stratified_split(self, samples: List[Dict]) -> Tuple[List[Dict], List[Dict], List[Dict]]:
        """
        Perform stratified split based on primary labels
        """
        # Group samples by primary label
        label_groups = defaultdict(list)
        for sample in samples:
            label = sample['primary_label']
            label_groups[label].append(sample)
        
        train_samples = []
        val_samples = []
        test_samples = []
        
        # Split each label group
        for label, group_samples in label_groups.items():
            random.shuffle(group_samples)
            
            n = len(group_samples)
            train_end = int(n * self.train_ratio)
            val_end = train_end + int(n * self.val_ratio)
            
            train_samples.extend(group_samples[:train_end])
            val_samples.extend(group_samples[train_end:val_end])
            test_samples.extend(group_samples[val_end:])
        
        # Shuffle final splits
        random.shuffle(train_samples)
        random.shuffle(val_samples)
        random.shuffle(test_samples)
        
        return train_samples, val_samples, test_samples
    
    def save_split(self, samples: List[Dict], filepath: str):
        """Save split to file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        print(f"✓ Saved {len(samples)} samples to {filepath}")
    
    def print_split_stats(self, train, val, test):
        """Print statistics for each split"""
        from collections import Counter
        
        print("\n" + "="*70)
        print("SPLIT STATISTICS")
        print("="*70)
        
        for name, split in [("TRAIN", train), ("VALIDATION", val), ("TEST", test)]:
            label_counts = Counter(s['primary_label'] for s in split)
            print(f"\n{name} ({len(split)} samples):")
            for label, count in sorted(label_counts.items()):
                pct = (count / len(split)) * 100 if split else 0
                print(f"  {label:20s}: {count:4d} ({pct:5.1f}%)")
        
        print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Split WebSafety Dataset into train/val/test'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input JSONL file'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output directory'
    )
    parser.add_argument(
        '--train-ratio',
        type=float,
        default=0.7,
        help='Training set ratio (default: 0.7)'
    )
    parser.add_argument(
        '--val-ratio',
        type=float,
        default=0.15,
        help='Validation set ratio (default: 0.15)'
    )
    parser.add_argument(
        '--test-ratio',
        type=float,
        default=0.15,
        help='Test set ratio (default: 0.15)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Random seed for reproducibility'
    )
    
    args = parser.parse_args()
    
    # Validate ratios
    if abs(args.train_ratio + args.val_ratio + args.test_ratio - 1.0) > 0.01:
        print("Error: Ratios must sum to 1.0")
        return
    
    # Load samples
    print(f"Loading samples from {args.input}...")
    samples = []
    with open(args.input, 'r', encoding='utf-8') as f:
        for line in f:
            samples.append(json.loads(line))
    
    print(f"✓ Loaded {len(samples)} samples")
    
    # Create splits
    splitter = DatasetSplitter(
        args.train_ratio,
        args.val_ratio,
        args.test_ratio,
        args.seed
    )
    
    print("\nCreating stratified splits...")
    train, val, test = splitter.stratified_split(samples)
    
    # Create output directory
    os.makedirs(args.output, exist_ok=True)
    
    # Save splits
    splitter.save_split(train, os.path.join(args.output, 'train.jsonl'))
    splitter.save_split(val, os.path.join(args.output, 'validation.jsonl'))
    splitter.save_split(test, os.path.join(args.output, 'test.jsonl'))
    
    # Print statistics
    splitter.print_split_stats(train, val, test)
    
    print(f"\n✓ Split complete! Files saved to {args.output}")


if __name__ == '__main__':
    from typing import Tuple
    main()
