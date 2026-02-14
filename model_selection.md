# Justification of Model Selection.

## Overview

This system groups heterogeneous enterprise security evidence to NIS2 Article 21 domains.  
Semantic interpretation but not key word detection is the major challenge.  
Statements can be indirectly described, synonyms can be used or meaning embedded in procedural language.

Thus, the model should be able to generalize to invisible phraseology of regulations without being provided with task-specific training data.

---

## Reasons why facebook/bart-large-mnli Was Chosen.

BART Large MNLI is applied to the project in the line of zero-shot classification.

---

## Key Reasons

### None of the labeled data available.
No publicly available data set currently exists to match arbitrary enterprise security text with official NIS2 domain names.

Fine-tuning or training BERT would take:  
curated annotations  
domain experts  
a lot of preparation time.

Zero-shot inference can be deployed instantly.

---

### Strong semantic reasoning
BART MNLI is conditioned on natural language inference.

It does not match words, but considers:

Is this statement logically true to be a part of a domain?

Example:

Every administrator is subject to MFA.

Although there are no domain keywords, the model realizes that this is about authentication and system security.

---

### Improved generalization over rule based pipelines.
There is a wide range of compliance language in organizations.

A rules or key word approach would:  
create many false positives  
fail on paraphrased controls.  
need manual updating on a regular basis.

Transformer inference is self-adaptive.

---

### Production feasibility
There is reasonable inference time in this model because it is CPU-run.

This enables it to be deployed without GPS, which is in accordance with actual enterprise constraints.

---

## Why Not Fine-Tuned BERT

Precision would be better but it would need:

good marked correspondences.  
legal/compliance validation  
when regulations change, maintenance is required.

Since the engineering window is 7 days, zero-shot classification offered the best tradeoff between feasibility and intelligence.

---

## Why Not a Pure NER Pipeline

Entity Recognition can be useful in the extraction of items like:

MFA  
encryption  
assets  
vulnerabilities

But entity detection is not sufficient to ascertain regulatory intent.

Example:

"Logs are archived annually"

NER can identify logs, yet it is up to semantic interpretation to determine whether these aid incident management or audit management.

Thus NER was viewed as supportive and not primary.

---

## Confidence Strategy

The model probability is considered to be the main signal.

As a secondary calibration, in order to stabilize outputs and minimize edge noise, the keyword density of domain vocabularies is applied.

This balances this hybrid approach:

semantic intelligence  
practical robustness

and without the use of arbitrary scoring.

---

## Known Tradeoffs

Since the model is not highly detailed to legal frameworks:

Similar terminology may be disoriented in some areas.  
Laws do not necessarily follow high similarity.

Therefore, the results are not to be certified automatically, but should be used by the analyst.

---

## Future Evolution Path

With more time and information, it is possible to improve the system with:

fined-tuning on accepted mappings.  
ontology-based ranking  
inter-document context modelling.  
human feedback loops  
continuous calibration

---

## Final Rationale

The selected strategy will maximize:

semantic capability  
explainability  
reproducibility  
deployment simplicity

under the project time-span.

It exhibits actual AI inference and at the same time is feasible within practical settings.
