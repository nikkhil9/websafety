"""
Template Expander - Multiplies templates with realistic variations
Expands base templates to 1000+ variations per language category
"""

import json
import random
from pathlib import Path

# Variation strategies for each category
VARIATIONS = {
    "safe": {
        "prefixes": ["", "Just ", "Finally ", "Honestly ", "Wow, ", "  ", "Literally "],
        "suffixes": ["!", ".", "", " :)", " lol", " haha", "  ✨", " ❤️"],
        "intensifiers": ["so ", "really ", "very ", "super ", "absolutely ", "totally ", ""],
    },
    "cyberbullying": {
        "intensifiers": ["totally ", "completely ", "absolutely ", "so ", "really ", ""],
        "suffixes": ["", " loser", " lol", " lmao", " haha", " idiot", "!!", " 😂"],
    },
    "hate_speech": {
        "prefixes": ["Honestly ", "Look, ", "The truth is ", "Face it, ", ""],
        "suffixes": ["!", ".", "!!", " Period.", " Facts."],
    },
    "sexual_content": {
        "suffixes": [" ;)", " 😘", "", " babe", " baby", " cutie", "~"],
    },
    "violence": {
        "intensifiers": ["gonna ", "will ", "should ", "need to ", ""],
        "suffixes": ["!", "!!", "", " right now", " immediately"],
    },
    "self_harm": {
        "prefixes": ["", "I think ", "Feeling like ", "Maybe ", "Probably "],
        "suffixes": ["...", ".", "", " anymore"],
    },
    "phishing": {
        "prefixes": ["URGENT: ", "ALERT: ", "Action Required: ", "Important: ", ""],
        "suffixes": ["!", "!!", " NOW", " ASAP", " immediately", "."],
    },
    "threat": {
        "intensifiers": ["better ", "should ", "gonna ", "will ", ""],
        "suffixes": ["!", "...", ".", " buddy", " pal"],
    },
    "malware": {
        "prefixes": ["WARNING: ", "ALERT: ", "Critical: ", "System: ", ""],
        "suffixes": ["!", "!!", " now", " immediately", "."],
    },
}

# Synonyms for variation
SYNONYMS = {
    "bad": ["terrible", "awful", "horrible", "worst", "poor"],
    "good": ["great", "excellent", "amazing", "wonderful", "fantastic"],
    "very": ["really", "so", "super", "extremely", "incredibly"],
    "people": ["folks", "guys", "everyone", "persons"],
}

def expand_template(template, category, count=10):
    """Generate variations of a template"""
    variations = {template}  # Start with original
    
    var_config = VARIATIONS.get(category, {})
    prefixes = var_config.get("prefixes", [""])
    suffixes = var_config.get("suffixes", [""])
    intensifiers = var_config.get("intensifiers", [""])
    
    while len(variations) < count:
        # Random modifications
        modified = template
        
        # Add prefix
        if random.random() < 0.3:
            modified = random.choice(prefixes) + modified
        
        # Add suffix
        if random.random() < 0.4:
            modified = modified.rstrip('.!?') + random.choice(suffixes)
        
        # Add intensifier
        if random.random() < 0.2 and intensifiers:
            words = modified.split()
            if len(words) > 2:
                insert_pos = random.randint(0, min(2, len(words)-1))
                words.insert(insert_pos, random.choice(intensifiers))
                modified = " ".join(words)
        
        # Minor typos (rare, for realism)
        if random.random() < 0.05 and category in ["social", "message"]:
            modified = add_typo(modified)
        
        variations.add(modified.strip())
    
    return list(variations)[:count]

def add_typo(text):
    """Add minor typo for social media realism"""
    typos = {
        "you": "u", "your": "ur", "are": "r", "to": "2", "for": "4",
        "the": "da", "and": "nd", "what": "wat", "that": "dat"
    }
    words = text.split()
    if len(words) > 3 and random.random() < 0.3:
        idx = random.randint(0, len(words)-1)
        if words[idx].lower() in typos:
            words[idx] = typos[words[idx].lower()]
    return " ".join(words)

def expand_templates_file(input_file, output_file, target_per_category):
    """Expand templates in a file"""
    print(f"\n📝 Expanding {input_file.name}...")
    
    with open(input_file, 'r', encoding='utf-8') as f:
        templates = json.load(f)
    
    expanded = {}
    
    for category, template_list in templates.items():
        current_count = len(template_list)
        needed = max(0, target_per_category - current_count)
        
        if needed == 0:
            expanded[category] = template_list
            print(f"  ✓ {category}: {current_count} (sufficient)")
            continue
        
        # Expand each template
        all_variations = set(template_list)
        variations_per_template = max(1, needed // max(len(template_list), 1)) + 1
        
        for template in template_list:
            new_vars = expand_template(template, category, variations_per_template)
            all_variations.update(new_vars)
        
        expanded[category] = list(all_variations)[:target_per_category]
        print(f"  ✓ {category}: {current_count} → {len(expanded[category])}")
    
    # Save expanded templates
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(expanded, f, ensure_ascii=False, indent=2)
    
    print(f"  💾 Saved to {output_file.name}")

def expand_all_templates():
    """Expand all language template files"""
    base_path = Path(__file__).parent
    
    # Target count per category
    # For 3000 samples total with 9 categories:
    # safe (25%) = 750, cyberbullying (15%) = 450, etc.
    targets = {
        "safe": 800,
        "cyberbullying": 500,
        "hate_speech": 400,
        "sexual_content": 350,
        "violence": 350,
        "self_harm": 300,
        "phishing": 300,
        "threat": 250,
        "malware": 200,
    }
    
    print("🚀 Expanding template files for 9K dataset generation")
    print(f"Target distribution: {targets}\n")
    
    for lang in ["english", "telenglish", "hinglish"]:
        input_file = base_path / f"templates_{lang}.json"
        output_file = base_path / f"templates_{lang}_expanded.json"
        
        if input_file.exists():
            # Calculate category-specific targets
            with open(input_file, 'r', encoding='utf-8') as f:
                current = json.load(f)
            
            # Expand based on current counts
            expand_templates_file(input_file, output_file, 500)  # 500 variations per category
        else:
            print(f"⚠️  {input_file} not found, skipping")
    
    print("\n✨ Template expansion complete!")
    print("Ready to generate 9,000 samples")

if __name__ == "__main__":
    expand_all_templates()
