"""
Interactive Annotation Tool for WebSafety Dataset

Allows human annotators to annotate samples following the guidelines.

Usage:
    python -m dataset.annotation.annotator --input dataset/raw/ --output dataset/annotated/ --annotator-id A001
"""

import json
import os
import argparse
from datetime import datetime
from typing import Dict, List, Optional
import sys


class Annotator:
    def __init__(self, input_dir: str, output_file: str, annotator_id: str):
        self.input_dir = input_dir
        self.output_file = output_file
        self.annotator_id = annotator_id
        self.annotations = []
        self.current_index = 0
        
        # Load existing progress if available
        if os.path.exists(output_file):
            with open(output_file, 'r', encoding='utf-8') as f:
                self.annotations = [json.loads(line) for line in f]
            print(f"Loaded {len(self.annotations)} existing annotations")
    
    def load_samples(self, filename: str) -> List[Dict]:
        """Load samples from JSONL file"""
        samples = []
        filepath = os.path.join(self.input_dir, filename)
        
        if not os.path.exists(filepath):
            print(f"File not found: {filepath}")
            return samples
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                samples.append(json.loads(line))
        
        return samples
    
    def display_sample(self, sample: Dict):
        """Display sample to annotator"""
        print("\n" + "="*70)
        print(f"Sample ID: {sample.get('id', 'N/A')}")
        print("="*70)
        print(f"\nTEXT: {sample.get('text', '')}")
        
        if sample.get('url'):
            print(f"URL: {sample['url']}")
        
        print("\n" + "-"*70)
    
    def get_primary_label(self) -> str:
        """Get primary label from annotator"""
        labels = [
            "1. safe",
            "2. phishing",
            "3. malware",
            "4. hate_speech",
            "5. cyberbullying",
            "6. sexual_content",
            "7. violence"
        ]
        
        print("\nPRIMARY LABEL:")
        for label in labels:
            print(f"  {label}")
        
        while True:
            choice = input("\nSelect number (1-7): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7']:
                return labels[int(choice)-1].split('. ')[1]
            print("Invalid choice. Please select 1-7.")
    
    def get_secondary_labels(self) -> List[str]:
        """Get secondary labels"""
        labels = [
            "spam", "scam", "harassment", "doxxing", "threat",
            "self_harm", "misinformation", "impersonation",
            "profanity", "sensitive_content"
        ]
        
        print("\nSECONDARY LABELS (optional):")
        for i, label in enumerate(labels, 1):
            print(f"  {i}. {label}")
        
        print("\nEnter numbers separated by commas (e.g., 1,3,5) or press Enter to skip:")
        choice = input("> ").strip()
        
        if not choice:
            return []
        
        selected = []
        try:
            numbers = [int(x.strip()) for x in choice.split(',')]
            for num in numbers:
                if 1 <= num <= len(labels):
                    selected.append(labels[num-1])
        except ValueError:
            print("Invalid input, skipping secondary labels")
        
        return selected
    
    def get_severity(self) -> str:
        """Get severity level"""
        print("\nSEVERITY:")
        print("  1. low")
        print("  2. medium")
        print("  3. high")
        
        while True:
            choice = input("\nSelect (1-3): ").strip()
            if choice == '1':
                return 'low'
            elif choice == '2':
                return 'medium'
            elif choice == '3':
                return 'high'
            print("Invalid choice. Please select 1-3.")
    
    def get_context(self) -> str:
        """Get context"""
        contexts = [
            "1. social_media", "2. email", "3. comment",
            "4. message", "5. forum", "6. review",
            "7. chat", "8. other"
        ]
        
        print("\nCONTEXT:")
        for ctx in contexts:
            print(f"  {ctx}")
        
        while True:
            choice = input("\nSelect (1-8): ").strip()
            if choice in ['1', '2', '3', '4', '5', '6', '7', '8']:
                return contexts[int(choice)-1].split('. ')[1]
            print("Invalid choice. Please select 1-8.")
    
    def get_language(self) -> str:
        """Get language"""
        print("\nLANGUAGE:")
        print("  1. en (English)")
        print("  2. hi (Hindi)")
        print("  3. en-hi (Hinglish)")
        print("  4. te (Telugu)")
        print("  5. en-te (Tenglish)")
        print("  6. other")
        
        while True:
            choice = input("\nSelect (1-6): ").strip()
            if choice == '1':
                return 'en'
            elif choice == '2':
                return 'hi'
            elif choice == '3':
                return 'en-hi'
            elif choice == '4':
                return 'te'
            elif choice == '5':
                return 'en-te'
            elif choice == '6':
                return 'other'
            print("Invalid choice. Please select 1-6.")
    
    def get_yes_no(self, question: str) -> bool:
        """Get yes/no answer"""
        while True:
            answer = input(f"\n{question} (y/n): ").strip().lower()
            if answer in ['y', 'yes']:
                return True
            elif answer in ['n', 'no']:
                return False
            print("Invalid input. Please enter y or n.")
    
    def get_confidence(self) -> float:
        """Get confidence score"""
        while True:
            try:
                score = input("\nConfidence (0.0-1.0): ").strip()
                score = float(score)
                if 0.0 <= score <= 1.0:
                    return score
                print("Please enter a value between 0.0 and 1.0")
            except ValueError:
                print("Invalid input. Please enter a decimal number.")
    
    def annotate_sample(self, sample: Dict) -> Dict:
        """Annotate a single sample"""
        self.display_sample(sample)
        
        # Get all annotations
        primary_label = self.get_primary_label()
        secondary_labels = self.get_secondary_labels()
        severity = self.get_severity()
        context = self.get_context()
        language = self.get_language()
        
        # Demographics
        print("\nTARGET DEMOGRAPHIC:")
        print("  1. children  2. teens  3. adults  4. all")
        demo_choice = input("Select (1-4): ").strip()
        demographics = {
            '1': 'children', '2': 'teens', '3': 'adults', '4': 'all'
        }
        target_demographic = demographics.get(demo_choice, 'all')
        
        # Boolean fields
        contains_pii = self.get_yes_no("Contains PII (personal info)?")
        requires_context = self.get_yes_no("Requires additional context?")
        is_sarcasm = self.get_yes_no("Is sarcasm/irony?")
        is_borderline = self.get_yes_no("Is borderline/edge case?")
        
        # Cultural context
        print("\nCULTURAL CONTEXT:")
        print("  1. indian  2. western  3. global  4. other  5. none")
        culture_choice = input("Select (1-5): ").strip()
        culture_map = {
            '1': 'indian', '2': 'western', '3': 'global',
            '4': 'other', '5': None
        }
        cultural_context = culture_map.get(culture_choice, 'global')
        
        # Confidence and notes
        confidence = self.get_confidence()
        notes = input("\nNotes (optional): ").strip()
        
        # Build annotated sample
        annotated = sample.copy()
        annotated.update({
            "primary_label": primary_label,
            "secondary_labels": secondary_labels,
            "severity": severity,
            "context": context,
            "language": language,
            "target_demographic": target_demographic,
            "contains_pii": contains_pii,
            "requires_context": requires_context,
            "is_sarcasm": is_sarcasm,
            "is_borderline": is_borderline,
            "cultural_context": cultural_context,
            "annotator_id": self.annotator_id,
            "annotation_confidence": confidence,
            "notes": notes,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
        
        return annotated
    
    def save_annotation(self, annotation: Dict):
        """Save single annotation"""
        with open(self.output_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(annotation, ensure_ascii=False) + '\n')
    
    def run_interactive(self, samples: List[Dict]):
        """Run interactive annotation session"""
        print("\n" + "="*70)
        print("WebSafety Dataset Annotation Tool")
        print("="*70)
        print(f"\nAnnotator ID: {self.annotator_id}")
        print(f"Total samples to annotate: {len(samples)}")
        print(f"Already annotated: {len(self.annotations)}")
        print(f"Remaining: {len(samples) - len(self.annotations)}")
        print("\nControls:")
        print("  - Answer questions for each sample")
        print("  - Type 'skip' to skip a sample")
        print("  - Type 'quit' to save and exit")
        print("="*70)
        
        input("\nPress Enter to start annotating...")
        
        for i, sample in enumerate(samples[len(self.annotations):], len(self.annotations)):
            try:
                annotated = self.annotate_sample(sample)
                self.save_annotation(annotated)
                self.annotations.append(annotated)
                
                print(f"\n✓ Saved annotation {i+1}/{len(samples)}")
                
                # Ask if want to continue
                if (i + 1) < len(samples):
                    cont = input("\nContinue to next sample? (y/n/q to quit): ").strip().lower()
                    if cont in ['n', 'no', 'q', 'quit']:
                        print(f"\n✓ Saved {len(self.annotations)} annotations to {self.output_file}")
                        break
                
            except KeyboardInterrupt:
                print(f"\n\n✓ Interrupted. Saved {len(self.annotations)} annotations.")
                break
        
        print(f"\n{'='*70}")
        print(f"Annotation session complete!")
        print(f"Total annotations: {len(self.annotations)}")
        print(f"Output file: {self.output_file}")
        print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Interactive annotation tool for WebSafety Dataset'
    )
    parser.add_argument(
        '--input',
        type=str,
        required=True,
        help='Input file (JSONL) with samples to annotate'
    )
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Output file (JSONL) for annotations'
    )
    parser.add_argument(
        '--annotator-id',
        type=str,
        required=True,
        help='Annotator ID (e.g., A001)'
    )
    
    args = parser.parse_args()
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Load samples
    if not os.path.exists(args.input):
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    with open(args.input, 'r', encoding='utf-8') as f:
        samples = [json.loads(line) for line in f]
    
    print(f"Loaded {len(samples)} samples from {args.input}")
    
    # Start annotation
    annotator = Annotator(
        os.path.dirname(args.input),
        args.output,
        args.annotator_id
    )
    annotator.run_interactive(samples)


if __name__ == '__main__':
    main()
