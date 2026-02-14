"""
Multilingual Web Safety Dataset Generator
Generates 9,000 samples: 3K English, 3K Telenglish, 3K Hinglish
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Category distribution (9 categories)
CATEGORY_DISTRIBUTION = {
    "safe": 0.25,
    "cyberbullying": 0.15,
    "hate_speech": 0.12,
    "sexual_content": 0.10,
    "violence": 0.10,
    "self_harm": 0.08,
    "phishing": 0.08,
    "threat": 0.07,
    "malware": 0.05
}

# Map internal categories to schema labels
LABEL_MAPPING = {
    "safe": "safe",
    "cyberbullying": "cyberbullying",
    "hate_speech": "hate_speech",
    "sexual_content": "sexual_content",
    "violence": "violence",
    "self_harm": "violence",
    "phishing": "phishing",
    "threat": "cyberbullying",
    "malware": "malware"
}

class MultilingualDatasetGenerator:
    def __init__(self, samples_per_language=3000):
        self.samples_per_language = samples_per_language
        self.generated_ids = set()
        self.used_texts = set()
        
    def load_templates(self, language):
        """Load templates from JSON file - try expanded first"""
        base_path = Path(__file__).parent
        
        # Try expanded templates first
        expanded_file = base_path / f"templates_{language}_expanded.json"
        base_file = base_path / f"templates_{language}.json"
        
        if expanded_file.exists():
            print(f"  Loading expanded templates for {language}")
            with open(expanded_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        elif base_file.exists():
            print(f"  Loading base templates for {language}")
            with open(base_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"  ⚠️  No templates found for {language}")
            return {}
    
    def generate_id(self):
        """Generate unique 8-digit ID"""
        while True:
            id_str = f"WS-{random.randint(10000000, 99999999):08d}"
            if id_str not in self.generated_ids:
                self.generated_ids.add(id_str)
                return id_str
    
    def get_secondary_labels(self, category):
        """Get appropriate secondary labels"""
        mapping = {
            "cyberbullying": [["harassment"], [], ["harassment", "threat"]],
            "phishing": [["scam"], ["scam", "spam"]],
            "malware": [["scam"], []],
            "threat": [["harassment", "threat"], ["threat"]],
            "sexual_content": [["harassment"], [], ["sensitive_content"]],
            "self_harm": [["self_harm"], ["threat", "self_harm"]],
            "hate_speech": [["harassment"], [], ["profanity"]],
        }
        return random.choice(mapping.get(category, [[]]))
    
    def create_sample(self, text, category, language):
        """Create a complete sample"""
        lang_map = {"english": "en", "telenglish": "en-te", "hinglish": "en-hi"}
        
        severity_map = {
            "safe": "low",
            "phishing": random.choice(["medium", "high"]),
            "malware": random.choice(["medium", "high"]),
            "violence": random.choice(["high", "high", "medium"]),
            "threat": "high",
            "sexual_content": random.choice(["high", "medium"]),
            "self_harm": "high",
            "cyberbullying": random.choice(["medium", "high", "low"]),
            "hate_speech": random.choice(["high", "medium"])
        }
        
        return {
            "id": self.generate_id(),
            "text": text,
            "url": None,
            "primary_label": LABEL_MAPPING[category],
            "secondary_labels": self.get_secondary_labels(category),
            "severity": severity_map[category],
            "context": random.choice(["social_media", "social_media", "message", "comment", "forum"]),
            "language": lang_map[language],
            "target_demographic": random.choice(["teens", "adults", "all"]),
            "contains_pii": False,
            "requires_context": category in ["hate_speech", "cyberbullying"],
            "is_sarcasm": False,
            "is_borderline": random.random() < 0.1,
            "cultural_context": "indian" if language != "english" else random.choice(["global", "global", "western"]),
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "source": f"generated_{language}",
            "annotator_id": "AUTO-GEN",
            "annotation_confidence": 0.95,
            "notes": f"Auto-generated {language} sample"
        }
    
    def generate_for_language(self, language, templates):
        """Generate samples for one language"""
        samples = []
        print(f"\n📝 Generating {language.upper()} samples...")
        
        for category, ratio in CATEGORY_DISTRIBUTION.items():
            target_count = int(self.samples_per_language * ratio)
            category_templates = templates.get(category, [])
            
            if not category_templates:
                print(f"⚠️  No templates for {category}, skipping")
                continue
            
            generated = 0
            attempts = 0
            max_attempts = target_count * 3
            
            while generated < target_count and attempts < max_attempts:
                attempts += 1
                template = random.choice(category_templates)
                
                # Avoid duplicates
                if template not in self.used_texts:
                    self.used_texts.add(template)
                    sample = self.create_sample(template, category, language)
                    samples.append(sample)
                    generated += 1
            
            print(f"  ✓ {category}: {generated}/{target_count}")
        
        return samples
    
    def generate_all(self):
        """Generate complete 9K dataset"""
        all_samples = []
        
        print("🚀 Starting multilingual dataset generation")
        print(f"Target: {self.samples_per_language * 3:,} samples total\n")
        
        for lang in ["english", "telenglish", "hinglish"]:
            try:
                templates = self.load_templates(lang)
                samples = self.generate_for_language(lang, templates)
                all_samples.extend(samples)
                print(f"✅ {len(samples):,} {lang} samples completed")
            except FileNotFoundError:
                print(f"❌ Template file for {lang} not found!")
        
        random.shuffle(all_samples)
        print(f"\n🎉 Total generated: {len(all_samples):,} samples")
        return all_samples
    
    def save(self, samples, output_file):
        """Save to JSONL"""
        with open(output_file, 'w', encoding='utf-8') as f:
            for sample in samples:
                f.write(json.dumps(sample, ensure_ascii=False) + '\n')
        print(f"💾 Saved to: {output_file}")

if __name__ == "__main__":
    gen = MultilingualDatasetGenerator(samples_per_language=3000)
    dataset = gen.generate_all()
    
    output = Path(__file__).parent.parent / "raw" / "websafety_9k_multilingual.jsonl"
    gen.save(dataset, output)
    
    print("\n✨ Dataset generation complete!")
