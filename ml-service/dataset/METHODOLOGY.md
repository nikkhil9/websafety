# WebSafety Dataset Methodology

**Research Methodology for Novel Web Safety Dataset Creation**

## Abstract

This document describes the methodology for creating the WebSafety dataset - a novel, multi-modal, contextual, and multilingual dataset for web safety research. Our approach combines synthesis from existing public datasets with original data collection and annotation, applying a comprehensive annotation schema that goes beyond traditional binary or simple multi-class classification.

## 1. Research Objectives

### Primary Objectives
1. Create a comprehensive web safety dataset with rich contextual metadata
2. Include multilingual support (English, Telugu, Tenglish) - underrepresented in current research
3. Address modern threats (2024-2026) missing from older datasets
4. Provide nuanced classification with severity levels and context information

### Secondary Objectives
- Enable research into context-aware safety classification
- Support multi-label and multi-task learning approaches
- Provide edge cases and borderline examples for robust model training
- Enable cultural context-aware safety detection

## 2. Dataset Design

### 2.1 Annotation Schema

Our schema extends beyond traditional approaches by including:

**Primary Classification**
- 7 primary categories: Safe, Phishing, Malware, Hate Speech, Cyberbullying, Sexual Content, Violence
- Moving beyond binary (safe/unsafe) to enable granular classification

**Secondary Labels**
- 10 additional tags for multi-label classification
- Captures overlapping characteristics (e.g., phishing + scam)

**Contextual Metadata**
- Severity levels (Low, Medium, High)
- Platform context (Social Media, Email, etc.)
- Target demographics
- Language and cultural context
- PII detection flags
- Sarcasm and borderline case markers

**Quality Metrics**
- Annotator confidence scores
- Inter-annotator agreement tracking
- Detailed notes for complex cases

### 2.2 Unique Contributions

1. **Multilingual Indian Context**
   - First major web safety dataset with substantial Telugu/Tenglish content
   - Cultural context annotations for Indian cyber threats
   - Code-mixed language support

2. **Temporal Relevance**
   - Focus on modern threats (2024-2026)
   - Current social media patterns
   - Updated phishing and cyberbullying tactics

3. **Rich Contextual Features**
   - 20+ metadata fields per sample
   - Context-dependent classification support
   - Edge case documentation

## 3. Data Collection

### 3.1 Source Datasets

We synthesize data from 9-10 existing public datasets:

#### Hate Speech & Toxic Content
1. **Davidson et al. Hate Speech Dataset**
   - ~25,000 tweets labeled for hate speech
   - Citation: Davidson et al. (2017)
   
2. **HateXplain**
   - ~20,000 posts with explanations
   - Multi-platform (Twitter, Gab, Reddit)
   
3. **Jigsaw Toxic Comment Classification**
   - ~160,000 Wikipedia comments
   - Multi-label toxic behavior

#### Cyberbullying
4. **Cyberbullying Detection Dataset**
   - Social media posts
   - Multiple platforms

5. **FormSpring Cyberbullying**
   - Questions/answers from FormSpring
   - ~12,000 posts

#### Phishing & Malware
6. **PhishTank Database**
   - Verified phishing URLs
   - Regularly updated community-sourced

7. **URLhaus**
   - Malware distribution URLs
   - Maintained by abuse.ch

8. **OpenPhish**
   - Phishing URL feed
   - Active threats

#### Spam
9. **SMS Spam Collection**
   - ~5,000 SMS messages
   - Ham/Spam labels

10. **Enron Email Dataset** (subset)
    - Legitimate emails for "safe" category
    - Professional communication examples

### 3.2 Original Data Collection

**Target**: 10,000-15,000 original samples (30-40% of total dataset)

**Sources**:
1. **Manual Curation**
   - Recent social media posts (public, anonymized)
   - Modern phishing examples
   - Current cyberbullying patterns

2. **Tenglish/Telugu Content**
   - Original collection from Indian platforms
   - Code-mixed social media content
   - Regional cyberbullying and scam patterns

3. **Edge Cases**
   - Sarcastic content
   - Context-dependent examples
   - Borderline cases for model robustness

**Ethical Considerations**:
- Only public data sources
- PII removal/anonymization
- No personally attributable content
- IRB approval for human subject data (if applicable)

### 3.3 Data Augmentation

Limited augmentation to preserve authenticity:
- Paraphrasing for diversity (< 10% of samples)
- Back-translation for multilingual samples
- No synthetic generation of harmful content

## 4. Annotation Process

### 4.1 Annotator Selection

**Requirements**:
- Age 18+
- Proficiency in English
- Telugu/Tenglish familiarity (for multilingual samples)
- Understanding of internet culture
- Passed training on annotation guidelines

**Number of Annotators**: 2-3 for inter-annotator agreement

### 4.2 Annotation Procedure

1. **Training Phase**
   - Study annotation guidelines
   - Practice on 50 training samples
   - Discuss edge cases with team
   - Achieve >80% agreement on training set

2. **Annotation Phase**
   - Each sample annotated by 2 annotators minimum
   - Interactive tool guides through schema
   - Mandatory confidence scores
   - Notes required for borderline cases

3. **Review Phase**
   - Automatic conflict detection
   - Third annotator for disagreements
   - Team discussion for complex cases

### 4.3 Quality Assurance

**Validation Checks**:
- Schema compliance (JSON schema validation)
- Logical consistency (e.g., safe content can't have high severity)
- PII detection and flagging
- Completeness checks

**Agreement Metrics**:
- Cohen's Kappa for pairwise agreement
- Fleiss' Kappa for multi-annotator agreement
- Target: Kappa > 0.7 (substantial agreement)

**Conflict Resolution**:
- Discussion and consensus for disagreements
- Third annotator vote for persistent conflicts
- Documentation of difficult cases

## 5. Data Processing

### 5.1 Cleaning Pipeline

1. **Deduplication**
   - Exact match removal
   - Fuzzy matching for near-duplicates
   - Preserve intentional variations

2. **Text Normalization**
   - Unicode normalization
   - Whitespace cleanup
   - Preserve intentional formatting (e.g., "URGENT!!!")

3. **URL Validation**
   - Format checking
   - Remove unreachable domains
   - Preserve structure for analysis

4. **PII Handling**
   - Automated PII detection
   - Manual review of flagged content
   - Anonymization or removal as appropriate

### 5.2 Balancing

**Strategy**: Stratified sampling to achieve balanced representation

**Target Distribution**:
- Safe: 30%
- Phishing: 10%
- Malware: 10%
- Hate Speech: 15%
- Cyberbullying: 15%
- Sexual Content: 10%
- Violence: 10%

**Methods**:
- Undersampling over-represented classes
- Preserve all samples of rare classes
- Maintain label distribution in edge cases

### 5.3 Dataset Splits

**Stratified Split**:
- Training: 70%
- Validation: 15%
- Test: 15%

**Stratification by**:
- Primary label
- Language (ensure Telugu/Tenglish in all splits)
- Severity

**Reproducibility**:
- Fixed random seed (42)
- Documented sample IDs in each split
- Version control for split assignments

## 6. Comparison with Existing Datasets

| Feature | Existing Datasets | WebSafety (Ours) |
|---------|------------------|------------------|
| **Size** | 5K-160K | 25-30K (target) |
| **Labels** | 2-6 categories | 7 primary + 10 secondary |
| **Languages** | English only (mostly) | English + Telugu + Tenglish ✓ |
| **Metadata** | Minimal (1-3 fields) | Rich (20+ fields) ✓ |
| **Temporal** | 2015-2020 | 2024-2026 ✓ |
| **Context** | Label only | Platform, severity, demographics ✓ |
| **Cultural** | Western-centric | Indian context included ✓ |
| **Edge Cases** | Rarely included | Explicitly  marked ✓ |
| **Multi-modal** | Text OR URLs | Combined text + URLs ✓ |

## 7. Validation & Benchmarking

### 7.1 Dataset Quality Metrics

- **Inter-annotator Agreement**: Kappa > 0.7
- **Confidence**: Mean confidence > 0.75
- **Completeness**: <1% missing required fields
- **Balance**: Max deviation from target <5%

### 7.2 Model Benchmarking

**Baseline Models**:
1. Traditional ML (TF-IDF + SVM)
2. BERT-base
3. DistilBERT
4. RoBERTa
5. Multilingual BERT (for Telugu/Tenglish)

**Evaluation Metrics**:
- Accuracy
- Precision, Recall, F1 (per-class and weighted)
- Confusion matrix
- Performance on edge cases separately

**Novel Contributions to Validate**:
- Impact of contextual metadata on performance
- Cross-lingual transfer (English ↔ Tenglish)
- Severity prediction accuracy
- Multi-label performance

## 8. Ethical Considerations

### 8.1 Data Ethics

- **Public Data Only**: No private or hacked data sources
- **Anonymization**: All PII removed or anonymized
- **Consent**: Where applicable, platforms' ToS allow research use
- **No Amplification**: Harmful content not distributed outside research context

### 8.2 Annotator Well-being

- **Content Warnings**: Clear warnings about disturbing content
- **Break Protocol**: Mandatory breaks every 30 minutes
- **Support**: Access to mental health resources
- **Compensation**: Fair compensation for annotation work

### 8.3 Dataset Usage

- **Research Only**: Clearly marked for academic research
- **Responsible Use**: Terms prohibit harmful applications
- **No Surveillance**: Not for mass surveillance or targeting individuals
- **Transparency**: Full methodology disclosure

## 9. Limitations & Future Work

### 9.1 Known Limitations

1. **Language Coverage**: Limited to English and Telugu/Tenglish
2. **Platform Coverage**: May not represent all platforms equally
3. **Temporal Drift**: Threats evolve; dataset needs periodic updates
4. **Cultural Bias**: Primarily Indian + Western contexts
5. **Size**: Smaller than some single-source datasets

### 9.2 Future Directions

1. **Expansion**: Additional languages (Marathi, Tamil, etc.)
2. **Modalities**: Image and video content integration
3. **Real-time**: Streaming dataset with continuous updates
4. **Crowdsourcing**: Scale annotation with crowdworkers
5. **Active Learning**: Prioritize high-value samples for annotation

## 10. Citation & Attribution

### Citing This Dataset

```bibtex
@dataset{websafety2026,
  title={WebSafety: A Multi-Modal, Contextual, and Multilingual Dataset for Web Safety Research},
  author={[Your Name]},
  year={2026},
  institution={[Your University]},
  note={Combines synthesis from 10 public datasets with original annotations}
}
```

### Source Dataset Citations

[Full citations for all 10 source datasets to be included]

## 11. Reproducibility

### Code & Scripts
- All collection scripts open-sourced
- Annotation tool provided
- Processing pipeline documented and versioned

### Documentation
- Complete annotation guidelines
- Sample IDs and split assignments published
- Annotator training materials available

### Versioning
- Version 1.0: Initial release
- Semantic versioning for updates
- Change log maintained

---

**Document Version**: 1.0  
**Last Updated**: January 26, 2026  
**Contact**: [Your Email]
