import uuid
import re
from services.classifier import classify_text
from services.reasoner import detect_control, build_reasoning


def analyze_document(text: str, source_type: str):
    """
    Split text into lines, run BART, enrich with reasoning.
    """
    analysis_id = str(uuid.uuid4())



# clean weird line breaks
    clean = re.sub(r"\n+", " ", text)

# split into sentences
    lines = re.split(r'(?<=[.!?])\s+', clean)

# remove tiny/noise lines
    lines = [l.strip() for l in lines if len(l.strip()) > 15]


    findings = []

    for line in lines:
        # run BART
        result = classify_text(line)

        domain = result["domain"]
        bart_conf = result["confidence"]

        # build explanation
        final_conf, reasoning = build_reasoning(line, domain, bart_conf)
        control = detect_control(line)

        findings.append({
            "source_text": line,
            "identified_control": control,
            "nis2_domain": domain,
            "confidence": round(final_conf, 4),
            "reasoning": reasoning,
            "model_score": round(bart_conf, 4),
            "inference_ms": round(result["inference_ms"], 2),
            "source_type": source_type
        })

    return {
        "analysis_id": analysis_id,
        "findings": findings,
        "model_metadata": {
            "model_type": "bart-zero-shot",
            "model_name": "facebook/bart-large-mnli"
        }
    }


