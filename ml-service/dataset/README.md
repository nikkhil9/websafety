# WebSafety Novel Dataset

**A Multi-Modal, Contextual, and Multilingual Dataset for Web Safety Research**

## Overview

This dataset represents a novel contribution to web safety research, combining multi-modal classification, rich contextual metadata, and multilingual support (English + Telugu/Tenglish) - features rarely found together in existing datasets.

### Key Innovations

🌍 **Multilingual & Cultural Context**
- English, Telugu, and code-mixed Tenglish samples
- Indian cultural context annotations
- Global and regional threat patterns

🏷️ **Multi-Label Classification**
- 7 primary categories (Safe, Phishing, Malware, Hate Speech, Cyberbullying, Sexual Content, Violence)
- 10 secondary labels (Spam, Scam, Harassment, etc.)
- 3 severity levels (Low, Medium, High)

📊 **Rich Contextual Metadata**
- Platform context (Social Media, Email, etc.)
- Target demographics
- Temporal relevance (2024-2026)
- PII detection flags
- Cultural context markers

🎯 **Edge Cases & Nuanced Content**
- Sarcasm and context-dependent samples
- Borderline cases for model robustness
- Educational vs harmful distinctions

## Dataset Statistics

**Target Size**: 25,000-30,000 samples
- ~15,000-20,000 from synthesized existing datasets (cited)
- ~10,000+ original manually collected samples (30-40% original contribution)

**Distribution** (Target):
- Safe: 30%
- Phishing: 10%
- Malware: 10%
- Hate Speech: 15%
- Cyberbullying: 15%
- Sexual Content: 10%
- Violence: 10%

**Languages**:
- English: 70%
- Telugu: 15%
- Tenglish: 15%

## Dataset Structure

Each sample follows this schema (see `schema.json`):

```json
{
  "id": "WS-00000001",
  "text": "Sample text content",
  "url": "https://example.com",
  "primary_label": "safe",
  "secondary_labels": [],
  "severity": "low",
  "context": "social_media",
  "language": "en",
  "target_demographic": "adults",
  "contains_pii": false,
  "requires_context": false,
  "is_sarcasm": false,
  "is_borderline": false,
  "cultural_context": "global",
  "timestamp": "2026-01-26T09:43:00Z",
  "source": "original",
  "annotator_id": "A001",
  "annotation_confidence": 0.95,
  "notes": ""
}
```

## Directory Structure

```
dataset/
├── README.md                          # This file
├── schema.json                        # JSON schema for validation
├── annotation_guidelines.md           # Human annotation guidelines
├── METHODOLOGY.md                     # Research methodology
├── STATISTICS.md                      # Auto-generated statistics
├── raw/                               # Raw collected data
│   ├── urls/                          # URL collections
│   ├── text/                          # Text collections
│   └── combined/                      # Multi-modal samples
├── annotated/                         # Human-annotated data
│   ├── annotations_annotator1.jsonl
│   ├── annotations_annotator2.jsonl
│   └── merged/                        # Consensus annotations
├── processed/                         # Processed & cleaned data
│   ├── train.jsonl                    # Training set (70%)
│   ├── validation.jsonl               # Validation set (15%)
│   └── test.jsonl                     # Test set (15%)
├── collectors/                        # Data collection scripts
│   ├── url_collector.py
│   ├── text_collector.py
│   └── augmentor.py
├── annotation/                        # Annotation tools
│   ├── annotator.py
│   ├── validator.py
│   └── merge_annotations.py
├── processing/                        # Processing pipeline
│   ├── cleaner.py
│   ├── balancer.py
│   ├── splitter.py
│   └── statistics.py
└── training/                          # Model training
    ├── train_custom.py
    └── evaluate_custom.py
```

## Usage

### 1. Collect Data

```bash
# Collect URLs from public sources
python -m dataset.collectors.url_collector --output raw/urls/

# Collect text from existing datasets
python -m dataset.collectors.text_collector --output raw/text/

# Augment data
python -m dataset.collectors.augmentor --input raw/ --output raw/augmented/
```

### 2. Annotate Data

```bash
# Start annotation interface
python -m dataset.annotation.annotator --input raw/ --output annotated/ --annotator-id A001

# Validate annotations
python -m dataset.annotation.validator --input annotated/ --schema schema.json

# Merge multiple annotators
python -m dataset.annotation.merge_annotations --input annotated/ --output annotated/merged/
```

### 3. Process Dataset

```bash
# Clean data
python -m dataset.processing.cleaner --input annotated/merged/ --output processed/cleaned.jsonl

# Balance categories
python -m dataset.processing.balancer --input processed/cleaned.jsonl --output processed/balanced.jsonl

# Create splits
python -m dataset.processing.splitter --input processed/balanced.jsonl --output processed/

# Generate statistics
python -m dataset.processing.statistics --input processed/ --output STATISTICS.md
```

### 4. Train Models

```bash
# Fine-tune transformer model
python -m dataset.training.train_custom \
  --train processed/train.jsonl \
  --val processed/validation.jsonl \
  --model distilbert-base-uncased \
  --output models/websafety-custom/

# Evaluate
python -m dataset.training.evaluate_custom \
  --model models/websafety-custom/ \
  --test processed/test.jsonl
```

## Data Sources

This dataset synthesizes and extends the following public datasets (properly cited):

1. **Hate Speech Detection**
   - Davidson et al. Hate Speech Dataset
   - HateXplain Dataset
   
2. **Cyberbullying**
   - Cyberbullying Detection Dataset
   - Social Media Cyberbullying Dataset

3. **Phishing & Malicious URLs**
   - PhishTank Database
   - URLhaus Malware URLs
   - OpenPhish Database

4. **Toxic Comments**
   - Jigsaw Toxic Comment Classification
   - Wikipedia Talk Pages

5. **Spam Detection**
   - SMS Spam Collection
   - Enron Email Dataset

**Plus**: 10,000+ originally collected and annotated samples

## Citation

If you use this dataset, please cite:

```bibtex
@dataset{websafety2026,
  title={WebSafety: A Multi-Modal, Contextual, and Multilingual Dataset for Web Safety Research},
  author={[Your Name]},
  year={2026},
  publisher={[University/Organization]}
}
```

## Ethical Considerations

- All data collected ethically from public sources
- PII is flagged and can be removed
- Harmful content included only for research purposes
- Annotator guidelines include content warning protocols
- Dataset should be used responsibly for safety research only

## License

[To be determined - typically CC BY-NC-SA 4.0 for research datasets]

## Contact

For questions or collaboration: [Your Email]
