import json
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOMAINS_PATH = BASE_DIR / "data" / "domains.json"

# Domain keyword lists for density scoring + reasoning
DOMAIN_KEYWORDS = {
    "Incident Handling": ["log", "logging", "monitor", "alert", "incident", "breach", "response", "siem", "forensic"],
    "Risk Assessment": ["vulnerability", "scan", "cve", "risk", "threat", "assessment", "remediation", "patch", "pentest"],
    "Supply Chain Security": ["vendor", "supplier", "third-party", "contract", "due diligence", "outsourcing", "sbom", "procurement"],
    "Network & Information System Security": ["encryption", "tls", "aes", "access", "iam", "mfa", "authentication", "authorization", "hardening", "segmentation"]
}

CONTROL_PATTERNS = [
    (r"\bmfa\b|\b2fa\b", "Multi-Factor Authentication (MFA)"),
    (r"\bencrypt|\btls\b|\baes\b|\bkey management\b", "Encryption / Cryptographic Protection"),
    (r"\blog\b|\blogging\b|\bmonitor\b|\bsiem\b|\baudit\b", "Audit Logging & Monitoring"),
    (r"\bvulnerab|\bcve\b|\bscan\b|\bpatch\b", "Vulnerability Management"),
    (r"\bvendor\b|\bsupplier\b|\bthird[- ]party\b|\bsbom\b", "Third-Party / Supply Chain Controls"),
    (r"\baccess control\b|\biam\b|\brole\b|\bpermission\b", "Access Control / IAM")
]

def keyword_density(text: str, domain: str) -> float:
    words = re.findall(r"[a-zA-Z0-9_-]+", text.lower())
    if not words:
        return 0.0
    kws = set(k.lower() for k in DOMAIN_KEYWORDS.get(domain, []))
    hits = sum(1 for w in words if w in kws)
    return min(1.0, hits / max(1, len(words)))

def detect_control(text: str) -> str:
    t = text.lower()
    for pat, label in CONTROL_PATTERNS:
        if re.search(pat, t):
            return label
    return "General NIS2 Control"

def build_reasoning(text: str, domain: str, bart_conf: float) -> tuple[float, str]:

    kd = keyword_density(text, domain)

    control = detect_control(text)
    control_bonus = 1.0 if control != "General NIS2 Control" else 0.0

    final_conf = (
    	0.6 * bart_conf +
    	0.25 * kd +
    	0.15 * control_bonus
    )

# reward strong semantic matches
    if bart_conf > 0.75:
    	final_conf += 0.1

    final_conf = max(0.0, min(1.0, final_conf))



    # show top matched keywords (for explanation)
    matched = []
    for kw in DOMAIN_KEYWORDS.get(domain, []):
        if kw.lower() in text.lower():
            matched.append(kw)
    matched = matched[:6]

    reasoning = (
        f"BART score={bart_conf:.3f}; keyword_density={kd:.3f}; "
        f"final_conf={final_conf:.3f}; matched_keywords={matched}"
    )
    return final_conf, reasoning

