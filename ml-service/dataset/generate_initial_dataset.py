"""
Quick Dataset Generator - Standalone version without external dependencies
Generates initial WebSafety dataset with Hinglish and Tenglish samples
"""

import json
import os
from datetime import datetime
import random

def generate_dataset(output_file="dataset/processed/websafety_initial.jsonl"):
    """Generate initial dataset"""
    
    print("="*60)
    print("WebSafety Dataset Generator")
    print("="*60)
    
    samples = []
    sample_id = 1
    
    # Safe samples
    safe_examples = [
        "Just finished a great book on machine learning!",
        "What's everyone having for dinner tonight?",
        "Check out this awesome sunset photo I took",
        "Happy birthday! Hope you have an amazing day!",
        "Meeting at 3pm tomorrow, don't forget",
    ]
    
    # Hate speech
    hate_examples = [
        "All [group] are criminals and should be deported",
        "[Religious group] are all terrorists",
        "Women belong in the kitchen",
    ]
    
    # Cyberbullying
    bully_examples = [
        "Nobody likes you, just go away",
        "You're so ugly, no wonder you have no friends",
        "Everyone hates you loser",
    ]
    
    # Phishing
    phish_examples = [
        "Your account has been locked. Click here to verify immediately",
        "Congratulations! You've won $1000. Enter your details to claim",
        "Urgent: Your payment failed. Update card details: http://fake-bank.tk",
    ]
    
    # Malware
    malware_examples = [
        "Download now to speed up your computer: http://free-optimizer.exe",
        "Click here to install free antivirus: http://malware-site.com/av.exe",
        "Your system is infected! Download this fix immediately",
    ]
    
    # Sexual content
    sexual_examples = [
        "Send me explicit photos or I'll share your secrets",
        "Click for adult content: [explicit-link]",
        "[Inappropriate solicitation]",
    ]
    
    # Violence
    violence_examples = [
        "I'm going to hurt you if you don't listen",
        "Someone should attack that place",
        "[Graphic threat of violence]",
    ]
    
    # Hinglish samples
    hinglish_examples = [
        ("Yaar, ye movie bahut acchi thi!", "safe"),
        ("Kal college mein milte hain bro", "safe"),
        ("Tu kitna ganda hai yaar, koi friend nahi hai tera", "cyberbullying"),
        ("Loser hai tu complete", "cyberbullying"),
        ("Aapka account block ho gaya hai, turant verify karo", "phishing"),
    ]
    
    # Tenglish samples
    tenglish_examples = [
        ("Abbai, ee movie chala bagundi ra!", "safe"),
        ("Repu college lo kaldam bro", "safe"),
        ("Nuvvu entha chetta vadu ra, evaru friends undaru neeku", "cyberbullying"),
        ("Loser vi nuvvu completely", "cyberbullying"),
        ("Mee account block ayyindi, immediately verify cheyandi", "phishing"),
    ]
    
    # Generate safe samples (English)
    for _ in range(200):
        text = random.choice(safe_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "safe",
            "secondary_labels": [],
            "severity": "low",
            "context": random.choice(["social_media", "comment", "message"]),
            "language": "en",
            "target_demographic": "all",
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate hate speech samples
    for _ in range(100):
        text = random.choice(hate_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "hate_speech",
            "secondary_labels": [],
            "severity": "high",
            "context": random.choice(["social_media", "comment", "forum"]),
            "language": "en",
            "target_demographic": "all",
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate cyberbullying samples
    for _ in range(100):
        text = random.choice(bully_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "cyberbullying",
            "secondary_labels": ["harassment"],
            "severity": random.choice(["medium", "high"]),
            "context": random.choice(["social_media", "message"]),
            "language": "en",
            "target_demographic": random.choice(["teens", "adults"]),
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate phishing samples
    for _ in range(100):
        text = random.choice(phish_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "phishing",
            "secondary_labels": ["scam"],
            "severity": "high",
            "context": random.choice(["email", "message"]),
            "language": "en",
            "target_demographic": "adults",
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate malware samples
    for _ in range(50):
        text = random.choice(malware_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "malware",
            "secondary_labels": ["scam"],
            "severity": "high",
            "context": random.choice(["email", "message", "download"]),
            "language": "en",
            "target_demographic": "adults",
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate sexual content samples
    for _ in range(50):
        text = random.choice(sexual_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "sexual_content",
            "secondary_labels": ["harassment"],
            "severity": "high",
            "context": random.choice(["message", "social_media"]),
            "language": "en",
            "target_demographic": random.choice(["teens", "adults"]),
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate violence samples
    for _ in range(50):
        text = random.choice(violence_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": "violence",
            "secondary_labels": ["threat"],
            "severity": "high",
            "context": random.choice(["message", "social_media", "comment"]),
            "language": "en",
            "target_demographic": "all",
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "global",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "generated",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Auto-generated sample"
        })
        sample_id += 1
    
    # Generate Hinglish samples
    for _ in range(100):
        text, label = random.choice(hinglish_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": label,
            "secondary_labels": ["harassment"] if label == "cyberbullying" else (["scam"] if label == "phishing" else []),
            "severity": "high" if label in ["cyberbullying", "phishing"] else "low",
            "context": "social_media",
            "language": "en-hi",
            "target_demographic": random.choice(["teens", "adults"]),
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "indian",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "original_hinglish",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Original Hinglish sample - UNIQUE"
        })
        sample_id += 1
    
    # Generate Tenglish samples
    for _ in range(100):
        text, label = random.choice(tenglish_examples)
        samples.append({
            "id": f"WS-{str(sample_id).zfill(8)}",
            "text": text,
            "url": None,
            "primary_label": label,
            "secondary_labels": ["harassment"] if label == "cyberbullying" else (["scam"] if label == "phishing" else []),
            "severity": "high" if label in ["cyberbullying", "phishing"] else "low",
            "context": "social_media",
            "language": "en-te",
            "target_demographic": random.choice(["teens", "adults"]),
            "contains_pii": False,
            "requires_context": False,
            "is_sarcasm": False,
            "is_borderline": False,
            "cultural_context": "indian",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": "original_tenglish",
            "annotator_id": "AUTO",
            "annotation_confidence": 1.0,
            "notes": "Original Tenglish sample - UNIQUE"
        })
        sample_id += 1
    
    # Shuffle
    random.shuffle(samples)
    
    # Create output directory
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    # Statistics
    label_counts = {}
    lang_counts = {}
    for sample in samples:
        label = sample["primary_label"]
        lang = sample["language"]
        label_counts[label] = label_counts.get(label, 0) + 1
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
    
    print(f"\n✓ Generated {len(samples)} samples")
    print(f"✓ Saved to: {output_file}")
    print("\nLabel Distribution:")
    for label, count in sorted(label_counts.items()):
        print(f"  {label}: {count}")
    print("\nLanguage Distribution:")
    for lang, count in sorted(lang_counts.items()):
        print(f"  {lang}: {count}")
    print("="*60)
    
    return output_file

if __name__ == "__main__":
    generate_dataset()
