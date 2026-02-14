# AI-Powered Multi-Source NIS2 Compliance Mapper

This project implements an AI system that automatically maps security evidence from enterprise documents into NIS2 Article 21 control domains.

The system accepts:

- PDF compliance reports  
- JSON API/configuration files  
- SQL database schemas  

and uses a transformer model to generate **confidence-scored, explainable classifications**.

---

## ✨ Features

- Multi-source ingestion (PDF / JSON / SQL)
- Zero-shot transformer classification using **facebook/bart-large-mnli**
- Automatic control identification (MFA, logging, encryption, IAM, etc.)
- Evidence-based confidence scoring
- REST API with FastAPI
- React dashboard
- Confidence threshold filtering
- Domain distribution chart
- Model metadata endpoint

---

## 🧠 AI Method

Each extracted sentence is:

1. Parsed from the input file  
2. Classified by BART zero-shot inference  
3. Calibrated with domain keyword density  
4. Returned with reasoning  

This ensures semantic understanding instead of simple keyword matching.

---

## 🏗 Architecture

1. **Ingestion Layer**: Handles PDF parsing, JSON loading, and SQL schema extraction.
2. **AI Classification Layer**: Runs BART inference and confidence calibration. 
3. **API Layer**: Exposes endpoints for classification and metadata.
4. **Frontend Layer**: React dashboard for visualization and interaction.

Upload File
    ↓
Parser (PDF / JSON / SQL)
    ↓
Sentence Extraction
    ↓
BART Zero-Shot Classification
    ↓
Keyword Calibration
    ↓
Confidence Score
    ↓
REST API
    ↓
Frontend Dashboard


---

## 📁 Project Structure

cybessure/
│
├── backend/
│ ├── main.py
│ ├── requirements.txt
│ ├── sample.sql
│ ├── test_input.txt
│ │
│ ├── data/
│ │ └── domains.json
│ │
│ ├── parsers/
│ │ ├── pdf_parser.py
│ │ ├── json_parser.py
│ │ └── sql_parser.py
│ │
│ └── services/
│ ├── analyzer.py
│ ├── classifier.py
│ └── reasoner.py
│
└── frontend/
├── src/
│ ├── App.jsx
│ └── main.jsx
├── package.json
└── vite.config.js


---

---

## ⚙️ System Requirements

- Python **3.11+**
- Node.js **18+**
- pip
- npm

---

---

# 🚀 QUICK START (Reviewer Friendly)

Follow these steps exactly.

---

##  Clone Repository

```bash
git clone <your-repo-url>
cd cybessure

cd backend
pip install -r requirements.txt

uvicorn main:app --reload

http://127.0.0.1:8000

http://127.0.0.1:8000/docs

```open a new terminal

```bash
cd frontend
npm install
npm run dev
http://localhost:5173

---

## Use the System

Upload PDF / JSON / SQL file
Wait for analysis
View domain mappings
Adjust confidence threshold
Inspect reasoning

---

API Reference:

POST /api/v1/analyze
Upload file.
Returns:
{ "analysis_id": "uuid" }

GET /api/v1/results/{id}
Returns findings.

GET /api/v1/domains
Lists NIS2 domains.

GET /api/v1/model/info
Model metadata.

---
## output

{
  "source_text": "We enforce MFA for all administrator accounts",
  "identified_control": "Multi-Factor Authentication (MFA)",
  "nis2_domain": "Network & Information System Security",
  "confidence": 0.72,
  "reasoning": "BART score=0.66; keyword_density=0.40"
}

---
confidence mapping:

| Score     | Interpretation  |
| --------- | --------------- |
| > 0.80    | Strong evidence |
| 0.60–0.80 | Likely          |
| 0.40–0.60 | Weak            |
| < 0.40    | Low             |

---

## limitations

The model is not fine-tuned on NIS2-specific corpora.
Therefore some mappings may reflect semantic similarity rather than strict legal intent.

Outputs should be considered decision support, not final compliance certification.

---
## Future Work

Domain fine-tuning
Ontology-guided ranking
Human-in-the-loop validation
Cross-document memory
Continuous calibration

---