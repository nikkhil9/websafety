"""
Validator for WebSafety Dataset

Validates dataset samples against the schema and performs quality checks.

Usage:
    python -m dataset.annotation.validator --input dataset/annotated/annotations.jsonl --schema dataset/schema.json
"""

import json
import os
import argparse
from typing import List, Dict, Tuple
import jsonschema
from collections import Counter, defaultdict


class DatasetValidator:
    def __init__(self, schema_path: str):
        with open(schema_path, 'r') as f:
            self.schema = json.load(f)
        
        self.validator = jsonschema.Draft7Validator(self.schema)
        self.errors = []
        self.warnings = []
    
    def validate_sample(self, sample: Dict, line_num: int) -> Tuple[bool, List[str]]:
        """Validate a single sample against schema"""
        errors = []
        
        try:
            # Schema validation
            validation_errors = list(self.validator.iter_errors(sample))
            if validation_errors:
                for error in validation_errors:
                    errors.append(f"Line {line_num}: {error.message} at {'.'.join(str(p) for p in error.path)}")
            
            # Additional business logic validation
            if sample.get('severity') == 'high' and sample.get('primary_label') == 'safe':
                errors.append(f"Line {line_num}: Safe content cannot have high severity")
            
            if sample.get('contains_pii') and not sample.get('notes'):
                self.warnings.append(f"Line {line_num}: PII flagged but no notes explaining")
            
            if sample.get('is_borderline') and sample.get('annotation_confidence', 1.0) > 0.7:
                self.warnings.append(f"Line {line_num}: Borderline case with high confidence seems contradictory")
            
        except Exception as e:
            errors.append(f"Line {line_num}: Validation error - {str(e)}")
        
        return len(errors) == 0, errors
    
    def validate_file(self, filepath: str) -> Dict:
        """Validate entire file"""
        print(f"Validating {filepath}...")
        
        valid_count = 0
        invalid_count = 0
        samples = []
        
        with open(filepath, 'r', encoding='utf-8') as f:
            for line_num, line in enumerate(f, 1):
                try:
                    sample = json.loads(line)
                    samples.append(sample)
                    
                    is_valid, errors = self.validate_sample(sample, line_num)
                    
                    if is_valid:
                        valid_count += 1
                    else:
                        invalid_count += 1
                        self.errors.extend(errors)
                
                except json.JSONDecodeError as e:
                    invalid_count += 1
                    self.errors.append(f"Line {line_num}: Invalid JSON - {str(e)}")
        
        return {
            'total': len(samples),
            'valid': valid_count,
            'invalid': invalid_count,
            'samples': samples
        }
    
    def calculate_inter_annotator_agreement(self, files: List[str]) -> float:
        """
        Calculate Cohen's Kappa for inter-annotator agreement
        (simplified version for demonstration)
        """
        if len(files) < 2:
            print("Need at least 2 annotator files to calculate agreement")
            return 0.0
        
        # Load all annotations
        all_annotations = {}
        for filepath in files:
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    sample = json.loads(line)
                    sample_id = sample.get('id')
                    if sample_id not in all_annotations:
                        all_annotations[sample_id] = []
                    all_annotations[sample_id].append(sample)
        
        # Find samples annotated by multiple annotators
        multi_annotated = {k: v for k, v in all_annotations.items() if len(v) > 1}
        
        if not multi_annotated:
            print("No samples were annotated by multiple annotators")
            return 0.0
        
        # Calculate agreement on primary labels
        agreements = 0
        total = 0
        
        for sample_id, annotations in multi_annotated.items():
            labels = [a['primary_label'] for a in annotations]
            # Check if all labels match
            if len(set(labels)) == 1:
                agreements += 1
            total += 1
        
        agreement_rate = agreements / total if total > 0 else 0.0
        
        print(f"Samples annotated by multiple annotators: {total}")
        print(f"Perfect agreement: {agreements} ({agreement_rate*100:.1f}%)")
        print(f"Note: This is simplified. For publication, use Cohen's Kappa or Fleiss' Kappa")
        
        return agreement_rate
    
    def generate_statistics(self, samples: List[Dict]) -> Dict:
        """Generate dataset statistics"""
        stats = {
            'total_samples': len(samples),
            'primary_labels': Counter(s['primary_label'] for s in samples),
            'severity': Counter(s['severity'] for s in samples),
            'context': Counter(s['context'] for s in samples),
            'language': Counter(s['language'] for s in samples),
            'contains_pii': sum(1 for s in samples if s.get('contains_pii')),
            'borderline_cases': sum(1 for s in samples if s.get('is_borderline')),
            'avg_confidence': sum(s.get('annotation_confidence', 0) for s in samples) / len(samples) if samples else 0,
        }
        
        return stats
    
    def print_report(self, stats: Dict):
        """Print validation report"""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)
        
        print(f"\nTotal Samples: {stats['total_samples']}")
        
        print("\nPrimary Labels:")
        for label, count in stats['primary_labels'].most_common():
            pct = (count / stats['total_samples']) * 100
            print(f"  {label:20s}: {count:5d} ({pct:5.1f}%)")
        
        print("\nSeverity:")
        for severity, count in stats['severity'].most_common():
            pct = (count / stats['total_samples']) * 100
            print(f"  {severity:10s}: {count:5d} ({pct:5.1f}%)")
        
        print("\nLanguage:")
        for lang, count in stats['language'].most_common():
            pct = (count / stats['total_samples']) * 100
            print(f"  {lang:10s}: {count:5d} ({pct:5.1f}%)")
        
        print(f"\nContains PII: {stats['contains_pii']}")
        print(f"Borderline Cases: {stats['borderline_cases']}")
        print(f"Average Confidence: {stats['avg_confidence']:.3f}")
        
        if self.errors:
            print(f"\n⚠ ERRORS: {len(self.errors)}")
            for error in self.errors[:10]:  # Show first 10
                print(f"  - {error}")
            if len(self.errors) > 10:
                print(f"  ... and {len(self.errors) - 10} more")
        else:
            print("\n✓ No validation errors!")
        
        if self.warnings:
            print(f"\n⚠ WARNINGS: {len(self.warnings)}")
            for warning in self.warnings[:10]:
                print(f"  - {warning}")
            if len(self.warnings) > 10:
                print(f"  ... and {len(self.warnings) - 10} more")
        
        print("="*70)


def main():
    parser = argparse.ArgumentParser(
        description='Validate WebSafety Dataset'
    )
    parser.add_argument(
        '--input',
        type=str,
        nargs='+',
        required=True,
        help='Input file(s) to validate (JSONL)'
    )
    parser.add_argument(
        '--schema',
        type=str,
        default='dataset/schema.json',
        help='Path to JSON schema file'
    )
    parser.add_argument(
        '--calculate-agreement',
        action='store_true',
        help='Calculate inter-annotator agreement (requires multiple input files)'
    )
    
    args = parser.parse_args()
    
    # Validate schema exists
    if not os.path.exists(args.schema):
        print(f"Error: Schema file not found: {args.schema}")
        return
    
    validator = DatasetValidator(args.schema)
    
    # Validate each file
    all_samples = []
    for filepath in args.input:
        if not os.path.exists(filepath):
            print(f"Error: File not found: {filepath}")
            continue
        
        result = validator.validate_file(filepath)
        all_samples.extend(result['samples'])
        
        print(f"✓ Validated {result['total']} samples")
        print(f"  Valid: {result['valid']}, Invalid: {result['invalid']}")
    
    # Generate statistics
    if all_samples:
        stats = validator.generate_statistics(all_samples)
        validator.print_report(stats)
    
    # Calculate inter-annotator agreement if requested
    if args.calculate_agreement and len(args.input) > 1:
        validator.calculate_inter_annotator_agreement(args.input)


if __name__ == '__main__':
    # Install jsonschema if not available
    try:
        import jsonschema
    except ImportError:
        print("Installing jsonschema...")
        os.system("pip install jsonschema")
        import jsonschema
    
    main()
