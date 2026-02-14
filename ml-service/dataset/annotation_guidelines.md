# WebSafety Dataset Annotation Guidelines

**Version 1.0 | Last Updated: January 2026**

## Purpose

These guidelines ensure consistent, high-quality annotations across all annotators. Please read carefully and refer back when uncertain.

## Before You Start

### Content Warning ⚠️

This dataset contains potentially disturbing content including:
- Hate speech and discriminatory language
- Cyberbullying and harassment
- Sexual content
- Violence and threats
- Scams and phishing attempts

**Take breaks as needed. Your mental health is important.**

### Annotator Requirements

- Proficiency in English
- Familiarity with Hindi/Hinglish and/or Telugu/Tenglish (for multilingual samples)
- Understanding of internet culture and social media
- Age 18+ (due to sensitive content)

## Annotation Process

### Step 1: Read the Content Carefully

- Read the full text/URL
- Consider the context provided
- Think about potential interpretations

### Step 2: Determine Primary Label

Choose **ONE** primary label that best describes the content:

#### 1. **Safe** 🟢
- Harmless content
- Appropriate for general audiences
- No malicious intent

**Examples:**
```
✓ "Check out this recipe for chocolate cake!"
✓ "Meeting at 3pm tomorrow, don't forget"
✓ "https://www.wikipedia.org"
```

#### 2. **Phishing** 🎣
- Attempts to steal credentials/personal info
- Fake login pages
- Impersonation of legitimate services

**Examples:**
```
✓ "Your bank account has been locked. Click here to verify: http://paypa1.com"
✓ "You've won $1000! Enter your SSN to claim"
✓ URLs mimicking legitimate sites (google.com → goog1e.com)
```

**Edge Cases:**
- Legitimate password reset emails → Safe
- Obvious joke phishing → Safe (if clearly satirical)

#### 3. **Malware** 🦠
- Malicious software distribution
- Downloads that harm devices
- Exploits and vulnerabilities

**Examples:**
```
✓ "Download free antivirus.exe here!"
✓ URLs to known malware sites
✓ "Click to install codec" (fake codec installers)
```

#### 4. **Hate Speech** 😠
- Attacks based on race, religion, ethnicity, gender, sexuality, disability
- Dehumanizing language
- Calls for violence against groups

**Examples:**
```
✓ "[Racial slur] should all be deported"
✓ "Women are too stupid to vote"
✓ "[Religious group] are terrorists"
```

**NOT Hate Speech:**
- Political criticism without targeting protected groups
- Profanity alone (mark as secondary label)
- Insults to individuals (may be cyberbullying)

**Cultural Context:**
- Consider Indian context (caste-based hate, religious tension)
- Some terms are hate speech in one culture but not another
- When in doubt, mark `requires_context: true`

#### 5. **Cyberbullying** 🎯
- Targeted harassment of individuals
- Repeated attacks or doxxing
- Threats of harm to specific people

**Examples:**
```
✓ "Kill yourself @username, nobody likes you"
✓ "Here's Sarah's address: 123 Main St. Let's go get her"
✓ "Look at this ugly loser *photo*"
```

**vs Hate Speech:**
- Hate speech targets a GROUP
- Cyberbullying targets an INDIVIDUAL
- Can sometimes overlap (mark both as secondary)

#### 6. **Sexual Content** 🔞
- Explicit sexual material
- Pornography or sexual solicitation
- Sexual harassment

**Examples:**
```
✓ Explicit anatomical descriptions
✓ "Send nudes or I'll..."
✓ Links to adult websites
```

**NOT Sexual Content:**
- Sex education (educational context)
- Medical discussions
- General dating/flirting

**Special Cases:**
- Unsolicited sexual content → High severity
- Educational content → Safe

#### 7. **Violence** ⚔️
- Graphic descriptions of violence
- Threats of physical harm
- Promotion of self-harm

**Examples:**
```
✓ "I'm going to shoot up the school tomorrow"
✓ Detailed torture descriptions
✓ "Cut yourself, it feels good"
```

### Step 3: Add Secondary Labels (Optional)

Select ALL that apply from:

- **spam**: Unsolicited bulk messages
- **scam**: Fraudulent schemes (not technically phishing)
- **harassment**: Persistent unwanted contact
- **doxxing**: Revealing private information
- **threat**: Explicit threats of harm
- **self_harm**: Promotion/encouragement of self-harm
- **misinformation**: Demonstrably false information
- **impersonation**: Pretending to be someone else
- **profanity**: Contains curse words/vulgar language
- **sensitive_content**: Disturbing but not clearly harmful

### Step 4: Determine Severity

#### Low 🟡
- Minimal harm potential
- Easily ignored or blocked
- No immediate danger

**Examples:**
- Mild spam
- Low-confidence phishing (obvious fake)
- Minor profanity

#### Medium 🟠
- Moderate harm potential
- Could affect some users
- Requires caution

**Examples:**
- Convincing phishing attempts
- Harassment without threats
- Hate speech without violence

#### High 🔴
- High harm potential
- Immediate danger or severe impact
- Requires urgent action

**Examples:**
- Credible threats of violence
- Advanced phishing targeting vulnerable users
- Doxxing with incitement
- Self-harm encouragement

### Step 5: Specify Context

Choose the most appropriate platform/context:

- **social_media**: Twitter, Facebook, Instagram, TikTok
- **email**: Email messages
- **comment**: Blog/YouTube/Reddit comments
- **message**: Private messaging (WhatsApp, DMs)
- **forum**: Discussion forums
- **review**: Product/service reviews
- **chat**: Real-time chat (Discord, IRC)
- **other**: Doesn't fit above categories

### Step 6: Set Language

- **en**: English only
- **hi**: Hindi only
- **en-hi**: Hinglish (code-mixed English + Hindi)
- **te**: Telugu only
- **en-te**: Tenglish (code-mixed English + Telugu)
- **other**: Other languages

**Hinglish Examples:**
```
"Yaar, ye scam hai kya?" (Friend, is this a scam?)
"Isko block kar do yaar" (Block this person, friend)
```

**Tenglish Examples:**
```
"Abbai, ee scam unda?" (Friend, is this a scam?)
"Veedu block chey bro" (Block this person, bro)
```

### Step 7: Additional Fields

#### Target Demographic
Who is the content primarily targeting or affecting?

- **children**: Under 13
- **teens**: 13-17
- **adults**: 18+
- **all**: No specific demographic

#### Contains PII
Does it include:
- Email addresses
- Phone numbers
- Physical addresses
- Social security numbers
- Any personally identifiable information

Mark `true` if yes.

#### Requires Context
Would understanding this content require additional information?

Examples requiring context:
- Sarcasm
- Cultural references
- Inside jokes
- Ambiguous statements

#### Is Sarcasm
Is the content using sarcasm or irony?

**Example:**
```
"Oh great, ANOTHER phishing email. Just what I needed today!"
(This is safe - person is complaining about phishing)
```

#### Is Borderline
Is this an edge case or difficult to classify?

Examples:
- Could be interpreted multiple ways
- Sits on the boundary between categories
- You're uncertain about classification

#### Cultural Context
- **indian**: Specifically relevant to Indian culture
- **western**: Western cultural context
- **global**: Universal/no specific culture
- **other**: Other specific cultural context

### Step 8: Confidence & Notes

#### Annotation Confidence
Rate 0.0 to 1.0 how confident you are:

- **0.9-1.0**: Very confident, clear case
- **0.7-0.8**: Fairly confident
- **0.5-0.6**: Uncertain, borderline
- **< 0.5**: Very uncertain (consider marking borderline)

#### Notes
Add any relevant comments:
- Why you chose this classification
- What made it difficult
- Cultural context explanations
- Questions for review

## Special Cases & FAQs

### Q: What if content has multiple harmful elements?

**A:** Choose the MOST SEVERE as primary, mark others as secondary.

Example: "I hate [group], here's their addresses, let's get them"
- Primary: `cyberbullying` or `hate_speech` (most prominent)
- Secondary: `doxxing`, `threat`
- Severity: `high`

### Q: What about obvious jokes or satire?

**A:** Consider intent and potential harm:
- Clear satire making fun of bad behavior → Safe
- "Joking" harassment that could hurt someone → Still harmful
- When in doubt: mark `requires_context: true` and add notes

### Q: Educational content about harmful things?

**A:** Context matters:
```
"This is an example of a phishing email: [example]" → Safe
"How to create phishing emails" → Malware/Harmful
```

### Q: Different cultural interpretations?

**A:** Use your best judgment based on:
- Your cultural knowledge
- Potential for harm in ANY culture
- Mark cultural_context appropriately
- Add notes explaining

### Q: Hinglish/Tenglish/code-mixed content?

**A:** 
- Mark language as `en-hi` for Hinglish or `en-te` for Tenglish
- Apply same rules as English content
- Consider Indian cultural context
- Note: Some Hindi/Telugu words might not translate severity-wise

### Q: URLs I can't verify?

**A:**
- DO NOT visit suspicious URLs
- Judge based on URL structure alone
- Known malicious indicators: typosquatting, suspicious TLDs, etc.
- Mark confidence lower if uncertain

### Q: Content about real events?

**A:**
- News reporting violence → Safe (if journalistic)
- Celebrating violence → Violence
- Threatening violence → Violence (high severity)

## Quality Checklist

Before submitting each annotation:

- [ ] Primary label selected
- [ ] Severity assigned
- [ ] Context specified
- [ ] Language set correctly
- [ ] All relevant secondary labels added
- [ ] Boolean flags set appropriately
- [ ] Confidence score reflects certainty
- [ ] Notes added for unclear cases
- [ ] No PII left unmasked (if flagged)

## Getting Help

If you encounter:

- **Technical issues**: Contact technical support
- **Classification questions**: Discuss with team lead
- **Disturbing content affecting you**: Take a break, access mental health resources
- **Unclear guidelines**: Request clarification before proceeding

## Examples - Full Annotations

### Example 1: Safe Content

```json
{
  "text": "Just finished reading a great book on machine learning!",
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
  "annotation_confidence": 1.0,
  "notes": "Clear safe content"
}
```

### Example 2: Phishing

```json
{
  "text": "Your Amazon account has been locked. Verify here: http://amaz0n-verify.tk",
  "url": "http://amaz0n-verify.tk",
  "primary_label": "phishing",
  "secondary_labels": ["scam", "impersonation"],
  "severity": "high",
  "context": "email",
  "language": "en",
  "target_demographic": "adults",
  "contains_pii": false,
  "requires_context": false,
  "is_sarcasm": false,
  "is_borderline": false,
  "cultural_context": "global",
  "annotation_confidence": 1.0,
  "notes": "Clear phishing attempt with typosquatting domain"
}
```

### Example 3: Cyberbullying (Hinglish)

```json
{
  "text": "Arre yaar tu kitna ganda hai, koi friend nahi hai tera. Kill yourself @username",
  "primary_label": "cyberbullying",
  "secondary_labels": ["harassment", "threat", "self_harm"],
  "severity": "high",
  "context": "social_media",
  "language": "en-hi",
  "target_demographic": "teens",
  "contains_pii": true,
  "requires_context": false,
  "is_sarcasm": false,
  "is_borderline": false,
  "cultural_context": "indian",
  "annotation_confidence": 1.0,
  "notes": "Direct attack on individual with self-harm encouragement. Contains username (PII)."
}
```

### Example 4: Borderline Hate Speech

```json
{
  "text": "These people are ruining our country with their backwards traditions",
  "primary_label": "hate_speech",
  "secondary_labels": [],
  "severity": "medium",
  "context": "comment",
  "language": "en",
  "target_demographic": "adults",
  "contains_pii": false,
  "requires_context": true,
  "is_sarcasm": false,
  "is_borderline": true,
  "cultural_context": "global",
  "annotation_confidence": 0.6,
  "notes": "Borderline - could be political critique or hate speech depending on context. Vague 'these people' could refer to political group or ethnic/religious group."
}
```

---

## Remember

- **Consistency is key** - use these guidelines for every annotation
- **When in doubt**, mark as borderline and add detailed notes
- **Take breaks** - this work can be emotionally taxing
- **Your annotations matter** - they directly impact model quality

Thank you for your careful work! 🙏
