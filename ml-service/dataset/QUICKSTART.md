# WebSafety Dataset - Quick Start Guide

This guide will help you quickly get started with creating and using the WebSafety dataset.

## Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Or manually:
pip install torch transformers datasets scikit-learn pandas jsonschema requests
```

## Step 1: Collect Initial Data (5 minutes)

Collect URL and text samples from simulated/public sources:

```bash
# Collect URLs (phishing, malware, safe)
python -m dataset.collectors.url_collector --output dataset/raw/urls/

# Collect text samples (hate speech, cyberbullying, etc.)
python -m dataset.collectors.text_collector --output dataset/raw/text/
```

**Output**: ~12,000+ simulated samples in `dataset/raw/`

## Step 2: Manual Annotation (Time-intensive)

For a research-grade dataset, you need to manually annotate samples:

```bash
# Start interactive annotation
python -m dataset.annotation.annotator \
  --input dataset/raw/text/all_text_samples.jsonl \
  --output dataset/annotated/annotations_A001.jsonl \
  --annotator-id A001
```

**Tips**:
- Read `annotation_guidelines.md` first
- Take breaks to avoid fatigue
- Aim for 100-200 samples per session
- Have  2-3 people annotate for inter-annotator agreement

**Shortcut for Testing**: The collected samples already have labels. You can skip this step for initial testing.

## Step 3: Validate Annotations

Check your annotations for quality and consistency:

```bash
# Validate against schema
python -m dataset.annotation.validator \
  --input dataset/annotated/annotations_A001.jsonl \
  --schema dataset/schema.json

# If you have multiple annotators:
python -m dataset.annotation.validator \
  --input dataset/annotated/annotations_A001.jsonl \
          dataset/annotated/annotations_A002.jsonl \
  --schema dataset/schema.json \
  --calculate-agreement
```

**Target Quality**:
- No schema validation errors
- Inter-annotator agreement (Kappa) > 0.7
- Mean confidence > 0.75

## Step 4: Process & Split Data

Combine all your data sources and create train/val/test splits:

```bash
# For demo purposes, combine the simulated data
cat dataset/raw/urls/all_urls.jsonl dataset/raw/text/all_text_samples.jsonl > dataset/processed/combined.jsonl

# Create stratified splits
python -m dataset.processing.splitter \
  --input dataset/processed/combined.jsonl \
  --output dataset/processed/ \
  --train-ratio 0.7 \
  --val-ratio 0.15 \
  --test-ratio 0.15
```

**Output**: 
- `dataset/processed/train.jsonl`
- `dataset/processed/validation.jsonl`
- `dataset/processed/test.jsonl`

## Step 5: Train Your Model

Fine-tune a transformer model on your custom dataset:

```bash
# Start training (this will take time depending on hardware)
python -m dataset.training.train_custom \
  --train dataset/processed/train.jsonl \
  --val dataset/processed/validation.jsonl \
  --model distilbert-base-uncased \
  --output models/websafety-custom \
  --epochs 3 \
  --batch-size 16
```

**Recommended Models**:
- `distilbert-base-uncased`: Fast, good performance
- `bert-base-uncased`: Better performance, slower
- `roberta-base`: Best performance, slowest
- `bert-base-multilingual-cased`: For Telugu/Tenglish support

**Hardware Requirements**:
- CPU: Works but slow (~1-2 hours per epoch)
- GPU (8GB): Recommended (~10-15 min per epoch)
- GPU (16GB+): Ideal, larger batch sizes

## Step 6: Evaluate Model

Test your trained model:

```bash
python -m dataset.training.evaluate_custom \
  --model models/websafety-custom \
  --test dataset/processed/test.jsonl
```

## Quick Test (End-to-End)

Want to test everything without waiting? Run this quick test:

```bash
# 1. Collect small sample
python -m dataset.collectors.text_collector --output dataset/raw/text/

# 2. Create a tiny split (first 100 samples)
head -n 100 dataset/raw/text/all_text_samples.jsonl > dataset/processed/tiny.jsonl

python -m dataset.processing.splitter \
  --input dataset/processed/tiny.jsonl \
  --output dataset/processed/

# 3. Quick train (1 epoch)
python -m dataset.training.train_custom \
  --train dataset/processed/train.jsonl \
  --val dataset/processed/validation.jsonl \
  --model distilbert-base-uncased \
  --output models/test-model \
  --epochs 1 \
  --batch-size 8
```

## Integration with WebSafety App

Once you've trained your custom model, integrate it:

### 1. Replace Text Classifier

```python
# In ml-service/models/text_classifier.py

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import json

class TextClassifier:
    def __init__(self):
        model_path = "models/websafety-custom"
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_path)
        
        # Load label mapping
        with open(f"{model_path}/label_mapping.json") as f:
            mapping = json.load(f)
            self.id2label = {int(k): v for k, v in mapping['id2label'].items()}
    
    def classify(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
        outputs = self.model(**inputs)
        predicted_class = outputs.logits.argmax(-1).item()
        confidence = torch.softmax(outputs.logits, dim=-1).max().item()
        
        return {
            "category": self.id2label[predicted_class],
            "confidence": confidence
        }
```

### 2. Update API

The model will now use your custom-trained model with the unique dataset!

## Directory Structure After Setup

```
dataset/
├── README.md
├── schema.json
├── annotation_guidelines.md
├── METHODOLOGY.md
├── raw/
│   ├── urls/
│   │   └── all_urls.jsonl (2,500 samples)
│   └── text/
│       └── all_text_samples.jsonl (12,000 samples)
├── annotated/ (if you did manual annotation)
│   └── annotations_A001.jsonl
├── processed/
│   ├── train.jsonl (70%)
│   ├── validation.jsonl (15%)
│   └── test.jsonl (15%)
├── collectors/
│   ├── url_collector.py
│   └── text_collector.py
├── annotation/
│   ├── annotator.py
│   └── validator.py
├── processing/
│   └── splitter.py
└── training/
    └── train_custom.py
```

## For Your Research Paper

After completing the dataset creation:

1. **Generate Statistics**:
   ```bash
   python -m dataset.annotation.validator \
     --input dataset/processed/*.jsonl \
     --schema dataset/schema.json
   ```

2. **Document Everything**:
   - Number of samples per category
   - Inter-annotator agreement scores
   - Annotation time statistics
   - Model performance metrics

3. **Key Claims for Your Paper**:
   - ✅ "We created a novel dataset of 25,000+ samples"
   - ✅ "First major web safety dataset with Tenglish support"
   - ✅ "Rich contextual metadata (20+ fields)"
   - ✅ "Achieved inter-annotator agreement of X (Kappa)"
   - ✅ "30%+ original, manually annotated contributions"
   - ✅ "Fine-tuned BERT achieving X% accuracy, outperforming baseline by Y%"

## Troubleshooting

### Issue: Out of Memory during training
```bash
# Reduce batch size
--batch-size 8  # or even 4
```

### Issue: Training too slow
```bash
# Use smaller model
--model distilbert-base-uncased  # instead of bert-base

# Reduce epochs
--epochs 2
```

### Issue: Low accuracy
- Collect more diverse samples
- Balance your dataset better
- Try different models
- Increase training epochs
- Add more original annotations

## Next Steps

1. **Scale Up**: Collect 25,000-30,000 samples as planned
2. **Get Annotators**: Recruit 2-3 annotators for quality
3. **Real Data**: Integrate actual datasets (HateXplain, PhishTank API, etc.)
4. **Multilingual**: Add more Telugu/Tenglish samples
5. **Publish**: Write your research paper with methodology
6. **Share**: Open-source your dataset (with appropriate licenses)

## Questions?

Check the full documentation:
- `README.md` - Dataset overview
- `METHODOLOGY.md` - Research methodology
- `annotation_guidelines.md` - Annotation instructions
- `schema.json` - Data structure

---

Happy researching! 🚀
