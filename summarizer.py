from groq import Groq
import os
import re


# ==========================
# GROQ CLIENT
# ==========================

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


# =========================================================
# DOMAIN & SUBDOMAIN KNOWLEDGE BASE
# =========================================================

DOMAIN_MAP = {
    "Artificial Intelligence": {
        "keywords": ["ai", "neural", "learning", "deep", "transformer", "ml", "intelligent"],
        "subdomains": {
            "Machine Learning": ["classification", "regression", "supervised", "unsupervised"],
            "Deep Learning": ["cnn", "rnn", "lstm", "gan", "transformer"],
            "Computer Vision": ["image", "vision", "object detection", "segmentation"],
            "Natural Language Processing": ["language", "text", "bert", "llm", "chatbot"],
            "Reinforcement Learning": ["reinforcement", "policy", "reward", "agent"]
        }
    },

    "Cybersecurity": {
        "keywords": ["attack", "security", "malware", "intrusion", "threat", "honeypot", "cyber"],
        "subdomains": {
            "Network Security": ["firewall", "ids", "ips", "network intrusion"],
            "Cryptography": ["encryption", "cipher", "rsa", "aes"],
            "Malware Analysis": ["trojan", "ransomware", "exploit"],
            "Digital Forensics": ["forensic", "investigation", "evidence"],
            "Cyber Deception": ["honeypot", "deception", "trap"]
        }
    }
}


ACADEMIC_KEYWORDS = [
    "model", "framework", "analysis", "approach",
    "method", "system", "design", "optimization",
    "prediction", "evaluation", "simulation",
    "performance", "dataset", "adaptive",
    "efficient", "novel", "dynamic",
    "comparative", "experimental", "hybrid",
    "architecture", "algorithm", "robust"
]


# =========================================================
# TEXT CLEANING
# =========================================================

def clean_text(text):
    text = re.sub(r"[^\w\s-]", "", text)
    return text.lower()


# =========================================================
# DOMAIN INFERENCE
# =========================================================

def infer_domains(title):
    t = clean_text(title)

    domain_scores = {}
    subdomains_detected = []

    for domain, data in DOMAIN_MAP.items():
        score = sum(1 for k in data["keywords"] if k in t)

        if score > 0:
            domain_scores[domain] = score

            for sub, sub_keys in data["subdomains"].items():
                if any(sk in t for sk in sub_keys):
                    subdomains_detected.append(sub)

    if not domain_scores:
        return ["General Research"], []

    sorted_domains = sorted(domain_scores, key=domain_scores.get, reverse=True)

    return sorted_domains, list(set(subdomains_detected))


# =========================================================
# RESEARCH TYPE
# =========================================================

def infer_research_type(title):
    t = title.lower()

    if "survey" in t or "review" in t:
        return "Survey / Review Paper"
    if "framework" in t or "model" in t:
        return "Proposed Framework / Model"
    if "dataset" in t:
        return "Dataset Contribution"
    if "evaluation" in t or "comparative" in t:
        return "Comparative Study"
    if "architecture" in t or "system" in t:
        return "System Architecture Design"
    return "Experimental Research"


# =========================================================
# NOVELTY
# =========================================================

def novelty_estimation(title):
    t = title.lower()

    if "novel" in t or "innovative" in t or "first" in t:
        return "High Innovation"
    if "adaptive" in t or "hybrid" in t or "robust" in t:
        return "Moderate to High Innovation"
    if "survey" in t or "review" in t:
        return "Knowledge Consolidation"
    return "Moderate Innovation"


# =========================================================
# CONFIDENCE
# =========================================================

def confidence_score(title):
    score = 0
    t = title.lower()

    for word in ACADEMIC_KEYWORDS:
        if word in t:
            score += 1

    length_factor = len(title.split()) // 3
    score += length_factor

    base = 70
    final_score = base + score * 2

    return min(98, max(65, final_score))


# =========================================================
# GROQ REFINEMENT (REPLACED OLLAMA)
# =========================================================

def llm_refinement(title, domains, subdomains, research_type):

    prompt = f"""
You are a senior academic research analyst.

Based ONLY on the title below, infer realistic research insights.

Title:
{title}

Primary Domains:
{', '.join(domains)}

Subdomains:
{', '.join(subdomains) if subdomains else "Not clearly specified"}

Research Type:
{research_type}

Write ONE professional academic paragraph explaining:
- objective
- methodology
- evaluation
- innovation
- impact
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4
        )

        return response.choices[0].message.content.strip()

    except Exception:
        return None


# =========================================================
# FALLBACK
# =========================================================

def fallback_paragraph(title, domains, research_type):
    return (
        f"This research appears to investigate {title.lower()}, situated within "
        f"{', '.join(domains)}. It likely represents a {research_type.lower()} "
        f"that develops structured methodologies supported by empirical evaluation. "
        f"The study may contribute theoretical advancements while also offering "
        f"practical implementation insights."
    )


# =========================================================
# MAIN
# =========================================================

def predict_contribution(title):

    domains, subdomains = infer_domains(title)
    research_type = infer_research_type(title)

    paragraph = llm_refinement(title, domains, subdomains, research_type)

    if not paragraph:
        paragraph = fallback_paragraph(title, domains, research_type)

    confidence = confidence_score(title)
    novelty = novelty_estimation(title)

    impact = (
        "This research may influence future investigations, inspire "
        "methodological refinement, and contribute to technological advancements."
    )

    return {
        "paragraph": paragraph,
        "confidence": confidence,
        "novelty": novelty,
        "impact": impact,
        "domains": domains,
        "subdomains": subdomains,
        "research_type": research_type
    }
