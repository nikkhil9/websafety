# 🛡️ WebSafety Project Presentation

**Title:** WebSafety: Multi-Indic Language Web Safety Classification  
**Subtitle:** Protecting Users in a Linguistically Diverse Digital Landscape  
**Presenter:** [Your Name]  

---

## 1. 🚨 The Problem
**Users are vulnerable in their native languages.**

*   **Gap:** Most web safety models (like ToxicBERT) are trained only on English data.
*   **Risk:** Malicious content in code-mixed Indian languages (Hinglish, Tenglish) goes undetected.
*   **Impact:** Millions of Indian users are exposed to phishing, bullying, and hate speech that filters miss.
*   **Example:** "Tu kitna ganda hai" (Hinglish bullying) is often classified as "Neutral/Safe" by English models.

---

## 2. 💡 Our Solution: WebSafety
**A specialized AI system for India's digital context.**

*   **Novel Dataset:** Custom-curated dataset specifically for code-mixed content.
*   **Multi-Modal:** Analyzes Text, URLs, and Images.
*   **Language Support:** English + Hinglish (Hindi-English) + Tenglish (Telugu-English).
*   **Granular Detection:** Identifies 7 specific threat categories, not just "Safe/Unsafe".

---

## 3. 📊 The Novel Dataset
**First of its kind for Web Safety in Tenglish/Hinglish.**

*   **Total Samples:** 850 manually annotated samples.
*   **Languages:**
    *   🇬🇧 English: 76.5%
    *   🇮🇳 Hinglish: 11.8%
    *   🇮🇳 Tenglish: 11.8%
*   **Categories (7 Classes):** 
    1. Safe
    2. Phishing
    3. Cyberbullying
    4. Hate Speech
    5. Malware
    6. Sexual Content
    7. Violence

---

## 4. 🧠 Methodology
**Transfer Learning with Transformers.**

*   **Base Model:** DistilBERT (Lightweight, Fast, Efficient).
*   **Training:** Fine-tuned on our custom 850-sample dataset.
*   **Infrastructure:** Trained on NVIDIA Tesla T4 GPU (Kaggle).
*   **Architecture:**
    *   *Input:* Tokenized Text (max len 512).
    *   *Process:* Transformer Layers extraction features.
    *   *Output:* 7-Class Probability Distribution.

---

## 5. 📈 Results & Performance
**High accuracy despite limited data.**

*   **Overall Accuracy:** **76.5%**
*   **Key Wins:**
    *   🛡️ **Cyberbullying:** 94% F1-Score (Excellent detection of harassment).
    *   🎣 **Phishing:** 84% F1-Score (High security against scams).
*   **Cross-Lingual Success:** Successfully detects "Yaar, ye link click mat karna" as Safe/Phishing context correctly.
*   **Training Time:** ~50 seconds (Extremely efficient).

*(Include `f1_scores_comparison.png` and `accuracy_chart.png` here)*

---

## 6. 🌐 System Demo
**End-to-End Web Application.**

1.  **User Interface:** React-based modern frontend.
2.  **Analyzers:**
    *   **Text:** Detects language and threat category.
    *   **URL:** Checks against phishing patterns.
    *   **Image:** Scans for NSFW content using ResNet50.
3.  **Real-Time:** Delivers safety verdict in milliseconds.

---

## 7. 🔮 Future Scope
**Scaling up for a safer internet.**

*   **More Data:** Expand to 10,000+ samples to improve Violence/Malware detection.
*   **More Languages:** Add Tanglish (Tamil), Manglish (Malayalam), etc.
*   **Context:** Analyze entire conversation threads, not just single messages.
*   **Deployment:** Browser extension for real-time protection on Social Media.

---

## 8. 🏁 Conclusion
**WebSafety bridges the gap.**

We successfully demonstrated that fine-tuning transformer models on a modest, specialized dataset can significantly improve safety for Indian language users, providing a foundation for more inclusive cybersecurity.

**Thank You!**
