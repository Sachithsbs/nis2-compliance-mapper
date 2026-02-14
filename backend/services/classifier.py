import json
import time
from transformers import pipeline
from pathlib import Path

# Load BART zero-shot model once
classifier = pipeline(
    "zero-shot-classification",
    model="facebook/bart-large-mnli"
)

# Load domain labels
BASE_DIR = Path(__file__).resolve().parent.parent
DOMAINS_PATH = BASE_DIR / "data" / "domains.json"

with open(DOMAINS_PATH, "r") as f:
    DOMAIN_DATA = json.load(f)

DOMAIN_LABELS = list(DOMAIN_DATA.keys())


def classify_text(text: str):
    """
    Runs zero-shot classification on input text.
    Returns domain + confidence + inference time.
    """
    start = time.time()

    result = classifier(
        text,
        DOMAIN_LABELS,
        multi_label=False
    )

    end = time.time()

    predicted_domain = result["labels"][0]
    confidence = float(result["scores"][0])

    return {
        "domain": predicted_domain,
        "confidence": confidence,
        "inference_ms": (end - start) * 1000
    }

