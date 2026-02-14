"""
Advanced Dataset Generator - Creates 9,000 realistic multilingual samples
Uses template patterns with intelligent variation
"""

import json
import random
from datetime import datetime
from pathlib import Path

# Pattern-based generation for each category

ENGLISH_PATTERNS = {
    "safe": {
        "social": ["Had {adj} time {activity}!", "{adv} finished {activity}", "{feeling} about {activity}",
                   "Meeting {people} for {activity}", "{adj} {thing} today", "Looking forward to {event}"],
        "questions": ["What's your favorite {thing}?", "Anyone tried {activity}?", "How do I {action}?",
                      "Best {thing} for {purpose}?", "Recommendations for {activity}?"],
        "news": ["{event} announced {thing}", "Study shows {finding}", "{organization} releases {thing}"],
    },
    "cyberbullying": {
        "insults": ["You're so {negative_adj}", "{negative_adj} and {negative_adj}", "Everyone {negative_action} you",
                    "Nobody {positive_action} you", "You're a {negative_noun}"],
        "exclusion": ["Don't {action} with us", "You're not {status}", "We're {activity}, you're not invited"],
    },
    "hate_speech": {
        "discrimination": ["{group} are all {negative}", "{group} don't belong here", "Our {thing} only",
                           "{group} should {negative_action}", "{group} are {negative_adj}"],
    },
    "sexual_content": {
        "harassment": ["You look {compliment}", "Send {request}", "Let's {suggestion}"],
        "spam": ["Hot {demographic} near you", "Click for {content}", "{service} free trial"],
    },
    "violence": {
        "threats": ["I'll {violent_action} you", "Someone should {violent_action} them",
                    "{violent_action} if you {condition}"],
    },
    "self_harm": {
        "ideation": ["I don't want to {live_verb} anymore", "{negative_feeling} is all I {verb}",
                     "Nobody would {care_verb} if I {action}"],
    },
    "phishing": {
        "urgent": ["Your {account} has been {status}! {action} now", "{alert}: {threat}. {instruction}"],
        "rewards": ["You've won {prize}! {action} to claim", "Free {item} - {instruction}"],
    },
    "threat": {
        "intimidation": ["Watch your {body_part}", "You're going to {negative_outcome}",
                         "I know where you {location}", "{negative_outcome} if you don't {comply}"],
    },
    "malware": {
        "fake_software": ["Download free {software}", "Your {system} is {problem}! {solution}",
                          "{software} update required"],
    },
}

# Fillers for patterns
FILLERS = {
    "adj": ["great", "amazing", "wonderful", "nice", "awesome", "fantastic", "lovely", "beautiful"],
    "adv": ["Just", "Finally", "Recently", "Totally", "Absolutely"],
    "activity": ["at the beach", "reading a book", "working out", "cooking", "studying", "shopping"],
    "feeling": ["Excited", "Happy", "Grateful", "Thankful", "Glad", "Pleased"],
    "people": ["friends", "family", "colleagues", "my team", "classmates"],
    "thing": ["book", "movie", "song", "place", "food", "app"],
    "event": ["concert", "party", "meetup", "conference", "game"],
    "action": ["learn", "fix", "improve", "understand", "solve"],
    "purpose": ["beginners", "students", "professionals", "learning"],
    "organization": ["Company", "Government", "University", "Team"],
    "finding": ["benefits of exercise", "new discovery", "important results"],
    
    "negative_adj": ["ugly", "stupid", "pathetic", "worthless", "useless", "dumb", "idiotic"],
    "negative_action": ["laughs at", "hates", "ignores", "avoids", "dislikes"],
    "positive_action": ["likes", "wants", "cares about", "supports"],
    "negative_noun": ["loser", "failure", "idiot", "fool", "joke"],
    "status": ["welcome", "invited", "wanted", "needed"],
    
    "group": ["Those people", "They", "Outsiders", "Immigrants", "That community"],
    "negative": ["criminals", "problems", "threats", "inferior", "wrong"],
    
    "compliment": ["hot", "sexy", "attractive"],
    "request": ["pics", "photos", "nudes"],
    "suggestion": ["meet up", "hang out alone", "have fun"],
    "demographic": ["singles", "people"],
    "content": ["adult content", "explicit material"],
    "service": ["Dating site", "Adult site"],
    
    "violent_action": ["hurt", "beat up", "attack", "punch", "destroy"],
    "condition": ["don't stop", "keep going", "continue"],
    
    "live_verb": ["live", "exist", "continue", "go on"],
    "negative_feeling": ["Pain", "Sadness", "Emptiness"],
    "verb": ["feel", "know", "understand"],
    "care_verb": ["care", "notice", "miss"],
    
    "account": ["account", "profile", "subscription"],
    "status": ["locked", "suspended", "compromised", "expired"],
    "alert": ["URGENT", "WARNING", "ALERT", "NOTICE"],
    "threat": ["Suspicious activity", "Security breach", "Unauthorized access"],
    "instruction": ["Click here", "Verify now", "Update immediately"],
    "prize": ["$10,000", "$5,000", "a prize", "a gift"],
    "item": ["iPhone", "gift card", "product"],
    
    "body_part": ["back", "step"],
    "negative_outcome": ["regret this", "pay", "suffer"],
    "location": ["live", "work", "are"],
    "comply": ["cooperate", "listen", "do what I say"],
    
    "software": ["optimizer", "cleaner", "antivirus", "driver"],
    "system": ["system", "computer", "device", "PC"],
    "problem": ["infected", "slow", "compromised"],
    "solution": ["Install this fix", "Download cleaner", "Run this scan"],
}

# Code-mixed patterns
TELENGLISH_PATTERNS = {
    "safe": ["Abbai, ee {thing} chala {adj} undi!", "{activity} repu {action}dam", "{thing} super undi"],
    "cyberbullying": ["Nuvvu chala {negative_adj} ga unnav", "{negative_action} evaru pattinchukoru"],
    "hate_speech": ["Mee {group} vallu antha {negative}", "Ee community acceptable kaadu"],
}

HINGLISH_PATTERNS = {
    "safe": ["Yaar, ye {thing} bahut {adj} hai!", "{activity} kal {action}te hain", "{thing} mast hai"],
    "cyberbullying": ["Tu bahut {negative_adj} hai", "{negative_action} koi tujhe nahi"],
    "hate_speech": ["Tumhare {group} log sab {negative}", "Ye community acceptable nahi"],
}

def fill_pattern(pattern, language="english"):
    """Fill a pattern  with random fillers"""
    result = pattern
    for key, values in FILLERS.items():
        placeholder = "{" + key + "}"
        if placeholder in result:
            result = result.replace(placeholder, random.choice(values))
    return result

def generate_samples_from_patterns(patterns, category, count, language):
    """Generate samples using patterns"""
    samples = []
    for _ in range(count):
        if isinstance(patterns, dict):
            # Choose random subcategory
            subcat = random.choice(list(patterns.keys()))
            pattern = random.choice(patterns[subcat])
        else:
            pattern = random.choice(patterns)
        
        text = fill_pattern(pattern, language)
        samples.append(text)
    
    return samples

def generate_dataset_advanced(output_file, samples_per_lang=3000):
    """Generate complete 9K dataset using patterns"""
    print("🚀 Generating 9,000 sample multilingual dataset")
    print(f"Distribution: 3,000 per language\n")
    
    all_samples = []
    sample_id = 100000
    
    # Distribution per language
    dist = {
        "safe": 750,
        "cyberbullying": 450,
        "hate_speech": 360,
        "sexual_content": 300,
        "violence": 300,
        "self_harm": 240,
        "phishing": 240,
        "threat": 210,
        "malware": 150,
    }
    
    for lang_name, lang_code, patterns in [
        ("English", "en", ENGLISH_PATTERNS),
        ("Telenglish", "en-te", TELENGLISH_PATTERNS),
        ("Hinglish", "en-hi", HINGLISH_PATTERNS),
    ]:
        print(f"\n📝 Generating {lang_name} samples ({samples_per_lang:,})...")
        
        for category, count in dist.items():
            if category not in patterns:
                # Use English patterns as fallback with language mixing
                patterns_to_use = ENGLISH_PATTERNS.get(category, ENGLISH_PATTERNS["safe"])
            else:
                patterns_to_use = patterns[category]
            
            texts = generate_samples_from_patterns(patterns_to_use, category, count, lang_name.lower())
            
            for text in texts:
                sample = create_sample(text, category, lang_code, sample_id)
                all_samples.append(sample)
                sample_id += 1
            
            print(f"  ✓ {category}: {count}")
    
    # Shuffle
    random.shuffle(all_samples)
    
    # Save
    with open(output_file, 'w', encoding='utf-8') as f:
        for sample in all_samples:
            f.write(json.dumps(sample, ensure_ascii=False) + '\n')
    
    print(f"\n✅ Generated {len(all_samples):,} samples")
    print(f"💾 Saved to: {output_file}")

def create_sample(text, category, lang_code, sample_id):
    """Create a sample dict"""
    label_map = {
        "safe": "safe", "cyberbullying": "cyberbullying", "hate_speech": "hate_speech",
        "sexual_content": "sexual_content", "violence": "violence", "self_harm": "violence",
        "phishing": "phishing", "threat": "cyberbullying", "malware": "malware"
    }
    
    severity_map = {
        "safe": "low", "phishing": "high", "malware": "high",
        "violence": "high", "threat": "high", "sexual_content": "high",
        "self_harm": "high", "cyberbullying": "medium", "hate_speech": "high"
    }
    
    return {
        "id": f"WS-{sample_id:08d}",
        "text": text,
        "url": None,
        "primary_label": label_map[category],
        "secondary_labels": [],
        "severity": severity_map.get(category, "medium"),
        "context": random.choice(["social_media", "message", "comment"]),
        "language": lang_code,
        "target_demographic": random.choice(["teens", "adults", "all"]),
        "contains_pii": False,
        "requires_context": category in ["hate_speech", "cyberbullying"],
        "is_sarcasm": False,
        "is_borderline": False,
        "cultural_context": "indian" if lang_code != "en" else "global",
        "timestamp": datetime.now().isoformat() + "Z",
        "source": f"generated_patterns_{lang_code}",
        "annotator_id": "AUTO",
        "annotation_confidence": 0.9,
        "notes": f"Pattern-based generation for {category}"
    }

if __name__ == "__main__":
    output = Path(__file__).parent.parent / "raw" / "websafety_9k_multilingual.jsonl"
    output.parent.mkdir(parents=True, exist_ok=True)
    generate_dataset_advanced(output, samples_per_lang=3000)
    print("\n✨ Dataset generation complete!")
