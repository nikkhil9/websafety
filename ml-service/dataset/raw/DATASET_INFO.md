# 9K Multilingual Web Safety Dataset

## Overview
Successfully generated **9,000 samples** for web safety classification training.

## Distribution

### Language Split
- **English**: 3,000 samples (`en`)
- **Telenglish** (Telugu + English): 3,000 samples (`en-te`)
- **Hinglish** (Hindi + English): 3,000 samples (`en-hi`)

### Category Distribution (per language)

| Category | Samples | Percentage |
|----------|---------|------------|
| Safe Content | 750 | 25% |
| Cyberbullying | 450 | 15% |
| Hate Speech | 360 | 12% |
| Sexual Content | 300 | 10% |
| Violence | 300 | 10% |
| Self-Harm | 240 | 8% |
| Phishing | 240 | 8% |
| Threats | 210 | 7% |
| Malware | 150 | 5% |
| **Total** | **3,000** | **100%** |

## Dataset Schema

Each sample includes:
- `id`: Unique identifier (WS-XXXXXXXX)
- `text`: The content to classify
- `primary_label`: Main category
- `secondary_labels`: Additional tags
- `severity`: Risk level (low/medium/high)
- `context`: Platform type
- `language`: Language code
- `cultural_context`: Cultural relevance
- `timestamp`: Generation timestamp
- Additional metadata fields

## Generation Method

- **Pattern-based generation** with intelligent template filling
- **Realistic variations** including:
  - Natural code-mixing for Hinglish/Telenglish
  - Context-appropriate language
  - Varied tones and styles
  - Social media-like formatting

## File Location

```
ml-service/dataset/raw/websafety_9k_multilingual.jsonl
```

## Next Steps

1. **Data Validation**: Review sample quality
2. **Train/Val/Test Split**: Create 70/15/15 splits
3. **Model Training**: Fine-tune transformer model
4. **Evaluation**: Test performance across languages

## Notes

- Balanced distribution across safety categories
- Equal representation of all three languages
- Suitable for multilingual content moderation
- Compatible with existing dataset schema
