"""
Text Collector for WebSafety Dataset

Synthesizes text samples from existing public datasets and applies
the WebSafety annotation schema.

Integrates samples from:
- Hate speech detection datasets
- Cyberbullying datasets
- Toxic comment datasets
- Spam detection datasets

Usage:
    python -m dataset.collectors.text_collector --output dataset/raw/text/
"""

import json
import os
import argparse
from datetime import datetime
from typing import List, Dict
import random


class TextCollector:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.sample_counter = 30000  # Start after URL IDs
    
    def get_next_id(self) -> str:
        """Generate next sample ID"""
        self.sample_counter += 1
        return f"WS-{str(self.sample_counter).zfill(8)}"
    
    def collect_hate_speech_samples(self, limit: int = 2000) -> List[Dict]:
        """
        Collect hate speech samples
        In production, would load from datasets like:
        - Davidson et al. Hate Speech Dataset
        - HateXplain
        """
        print(f"Collecting {limit} hate speech samples...")
        samples = []
        
        # Simulated examples (replace with real dataset loading)
        hate_speech_examples = [
            "All [group] are criminals and should be deported",
            "I hate [group], they're ruining our country",
            "[Religious group] are all terrorists",
            "Women belong in the kitchen, not in office",
            "[Ethnic slur] go back to your country",
        ]
        
        for i in range(min(limit, len(hate_speech_examples) * 10)):
            text = random.choice(hate_speech_examples)
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": "hate_speech",
                "secondary_labels": [],
                "severity": random.choice(["medium", "high"]),
                "context": random.choice(["social_media", "comment", "forum"]),
                "language": "en",
                "target_demographic": "all",
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": random.random() < 0.1,  # 10% borderline
                "cultural_context": random.choice(["global", "western"]),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "hate_speech_dataset_simulated",
                "notes": "Sample from hate speech dataset"
            })
        
        print(f"✓ Collected {len(samples)} hate speech samples")
        return samples
    
    def collect_cyberbullying_samples(self, limit: int = 2000) -> List[Dict]:
        """Collect cyberbullying samples"""
        print(f"Collecting {limit} cyberbullying samples...")
        samples = []
        
        cyberbullying_examples = [
            "Nobody likes you @username, just kill yourself",
            "@user you're so ugly, no wonder you have no friends",
            "Everyone hates you @username, go away",
            "@user is a loser and everyone knows it",
            "Look at this pathetic person @username *laughing emoji*",
        ]
        
        for i in range(min(limit, len(cyberbullying_examples) * 10)):
            text = random.choice(cyberbullying_examples)
            contains_pii = "@" in text
            secondary = ["harassment"]
            if "kill yourself" in text.lower():
                secondary.append("self_harm")
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": "cyberbullying",
                "secondary_labels": secondary,
                "severity": "high" if "kill" in text.lower() else random.choice(["medium", "high"]),
                "context": random.choice(["social_media", "comment", "message"]),
                "language": "en",
                "target_demographic": random.choice(["teens", "adults"]),
                "contains_pii": contains_pii,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "global",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "cyberbullying_dataset_simulated",
                "notes": "Sample from cyberbullying dataset"
            })
        
        print(f"✓ Collected {len(samples)} cyberbullying samples")
        return samples
    
    def collect_sexual_content_samples(self, limit: int = 1000) -> List[Dict]:
        """Collect sexual content samples"""
        print(f"Collecting {limit} sexual content samples...")
        samples = []
        
        # Using placeholder to avoid explicit content
        sexual_examples = [
            "Send me nudes or I'll share your photos",
            "Hey baby, wanna see something? *explicit link*",
            "[Explicit solicitation]",
            "Click here for free adult content: [link]",
        ]
        
        for i in range(min(limit, len(sexual_examples) * 10)):
            text = random.choice(sexual_examples)
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": "sexual_content",
                "secondary_labels": ["harassment"] if "send" in text.lower() else [],
                "severity": "high",
                "context": random.choice(["message", "social_media", "chat"]),
                "language": "en",
                "target_demographic": random.choice(["adults", "teens"]),
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "global",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "sexual_content_dataset_simulated",
                "notes": "Sexual content sample"
            })
        
        print(f"✓ Collected {len(samples)} sexual content samples")
        return samples
    
    def collect_violence_samples(self, limit: int = 1000) -> List[Dict]:
        """Collect violence/threat samples"""
        print(f"Collecting {limit} violence samples...")
        samples = []
        
        violence_examples = [
            "I'm going to shoot up the school tomorrow",
            "You better watch your back, I know where you live",
            "Someone should bomb that place",
            "[Graphic description of violence]",
            "I will hurt you if you don't do what I say",
        ]
        
        for i in range(min(limit, len(violence_examples) * 10)):
            text = random.choice(violence_examples)
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": "violence",
                "secondary_labels": ["threat"],
                "severity": "high",
                "context": random.choice(["social_media", "message", "comment"]),
                "language": "en",
                "target_demographic": "all",
                "contains_pii": "you live" in text,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "global",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "violence_dataset_simulated",
                "notes": "Violence/threat sample"
            })
        
        print(f"✓ Collected {len(samples)} violence samples")
        return samples
    
    def collect_safe_samples(self, limit: int = 5000) -> List[Dict]:
        """Collect safe content samples"""
        print(f"Collecting {limit} safe samples...")
        samples = []
        
        safe_examples = [
            "Just finished a great book on machine learning!",
            "What's everyone having for dinner tonight?",
            "Check out this awesome sunset photo I took",
            "Does anyone know a good recipe for pasta?",
            "Happy birthday! Hope you have an amazing day!",
            "This is a really helpful tutorial, thanks for sharing",
            "Meeting at 3pm tomorrow, don't forget",
            "I love this song! It's so catchy",
            "Can someone help me with this homework problem?",
            "Congratulations on your new job!",
        ]
        
        for i in range(min(limit, len(safe_examples) * 100)):
            text = random.choice(safe_examples)
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": "safe",
                "secondary_labels": [],
                "severity": "low",
                "context": random.choice(["social_media", "comment", "message", "forum"]),
                "language": "en",
                "target_demographic": "all",
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "global",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "safe_content_curated",
                "notes": "Safe content sample"
            })
        
        print(f"✓ Collected {len(samples)} safe samples")
        return samples
    
    def collect_hinglish_samples(self, limit: int = 1000) -> List[Dict]:
        """Collect Hindi/Hinglish samples (UNIQUE CONTRIBUTION!)"""
        print(f"Collecting {limit} Hinglish samples...")
        samples = []
        
        hinglish_examples = [
            # Safe
            ("Yaar, ye movie bahut acchi thi!", "safe", "low", []),
            ("Kal college mein milte hain bro", "safe", "low", []),
            ("Kya baat hai! Awesome work dude", "safe", "low", []),
            
            # Cyberbullying
            ("Tu kitna ganda hai yaar, koi friend nahi hai tera", "cyberbullying", "medium", ["harassment"]),
            ("Loser hai tu complete, everyone hates you", "cyberbullying", "high", ["harassment"]),
            
            # Hate Speech
            ("[Group] log bahut kharab hain, inko nikalo", "hate_speech", "high", []),
            
            # Scam/Phishing (common in North India)
            ("Aapka account block ho gaya hai, turant verify karo: [link]", "phishing", "high", ["scam"]),
            ("Congratulations! Aapne lottery jeet li, details bharne ke liye click karo", "phishing", "medium", ["scam"]),
        ]
        
        for i in range(min(limit, len(hinglish_examples) * 20)):
            text, label, severity, secondary = random.choice(hinglish_examples)
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": label,
                "secondary_labels": secondary,
                "severity": severity,
                "context": random.choice(["social_media", "message", "chat"]),
                "language": "en-hi",
                "target_demographic": random.choice(["teens", "adults"]),
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "indian",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "original_hinglish",
                "notes": "Original Hinglish sample - unique contribution"
            })
        
        print(f"✓ Collected {len(samples)} Hinglish samples")
        return samples
    
    def collect_tenglish_samples(self, limit: int = 1000) -> List[Dict]:
        """Collect Telugu/Tenglish samples (UNIQUE CONTRIBUTION!)"""
        print(f"Collecting {limit} Tenglish samples...")
        samples = []

        
        tenglish_examples = [
            # Safe
            ("Abbai, ee movie chala bagundi ra!", "safe", "low", []),
            ("Repu college lo kaldam bro", "safe", "low", []),
            ("Baundi! Awesome work ra", "safe", "low", []),
            
            # Cyberbullying
            ("Nuvvu entha chetta vadu ra, evaru friends undaru neeku", "cyberbullying", "medium", ["harassment"]),
            ("Loser vi nuvvu completely, everyone hates you", "cyberbullying", "high", ["harassment"]),
            
            # Hate Speech
            ("[Group] vallu chala chetta valu, vallani vellagottali", "hate_speech", "high", []),
            
            # Scam/Phishing (common in Telugu regions)
            ("Mee account block ayyindi, immediately verify cheyandi: [link]", "phishing", "high", ["scam"]),
            ("Congratulations! Meeru lottery gelicharu, details fill cheyandi", "phishing", "medium", ["scam"]),
        ]
        
        for i in range(min(limit, len(tenglish_examples) * 20)):
            text, label, severity, secondary = random.choice(tenglish_examples)
            
            samples.append({
                "id": self.get_next_id(),
                "text": text,
                "url": None,
                "primary_label": label,
                "secondary_labels": secondary,
                "severity": severity,
                "context": random.choice(["social_media", "message", "chat"]),
                "language": "en-te",
                "target_demographic": random.choice(["teens", "adults"]),
                "contains_pii": False,
                "requires_context": False,
                "is_sarcasm": False,
                "is_borderline": False,
                "cultural_context": "indian",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "source": "original_tenglish",
                "notes": "Original Tenglish sample - unique contribution"
            })
        
        print(f"✓ Collected {len(samples)} Tenglish samples")
        return samples
    
    def save_samples(self, samples: List[Dict], filename: str):
        """Save samples to JSONL file"""
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        print(f"✓ Saved {len(samples)} samples to {filepath}")
    
    def collect_all(self):
        """Collect all text sample types"""
        print("=" * 60)
        print("WebSafety Text Collector")
        print("=" * 60)
        
        all_samples = []
        
        # Collect each category
        all_samples.extend(self.collect_hate_speech_samples(2000))
        all_samples.extend(self.collect_cyberbullying_samples(2000))
        all_samples.extend(self.collect_sexual_content_samples(1000))
        all_samples.extend(self.collect_violence_samples(1000))
        all_samples.extend(self.collect_safe_samples(4000))
        all_samples.extend(self.collect_hinglish_samples(1000))
        all_samples.extend(self.collect_tenglish_samples(1000))
        
        # Shuffle
        random.shuffle(all_samples)
        
        # Save all
        self.save_samples(all_samples, "all_text_samples.jsonl")
        
        # Print summary
        print("\n" + "=" * 60)
        print("Collection Summary:")
        label_counts = {}
        for sample in all_samples:
            label = sample["primary_label"]
            label_counts[label] = label_counts.get(label, 0) + 1
        
        for label, count in sorted(label_counts.items()):
            print(f"  {label.title()}: {count}")
        print(f"  Total: {len(all_samples)}")
        print("=" * 60)
        print("\n📝 Note: This is simulated data for demonstration.")
        print("For production, load real datasets:")
        print("  - HateXplain: https://github.com/hate-alert/HateXplain")
        print("  - Jigsaw Toxic: https://www.kaggle.com/c/jigsaw-toxic-comment-classification-challenge")
        print("  - Cyberbullying: Various sources on Kaggle")


def main():
    parser = argparse.ArgumentParser(
        description='Collect text samples for WebSafety Dataset'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='dataset/raw/text',
        help='Output directory for collected text samples'
    )
    
    args = parser.parse_args()
    
    collector = TextCollector(args.output)
    collector.collect_all()


if __name__ == '__main__':
    main()
