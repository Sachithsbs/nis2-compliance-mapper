import uuid
import time
from datetime import datetime
from pathlib import Path
import json

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Parsers
from parsers.pdf_parser import parse_pdf
from parsers.json_parser import parse_json
from parsers.sql_parser import parse_sql

# Analyzer
from services.analyzer import analyze_document


# =====================================================
# App
# =====================================================

app = FastAPI(
    title="Cybessure NIS2 Compliance Mapper",
    version="1.0",
    description="BART-powered AI mapping of compliance evidence"
)

# Frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# temporary memory storage
RESULTS_DB = {}


# =====================================================
# Helpers
# =====================================================

def get_extension(filename: str) -> str:
    return filename.split(".")[-1].lower()


# =====================================================
# Routes
# =====================================================

@app.get("/")
def health():
    return {"status": "running"}


# -----------------------------------------------------
# POST /api/v1/analyze
# -----------------------------------------------------
@app.post("/api/v1/analyze")
async def analyze(file: UploadFile = File(...)):
    start = time.time()

    try:
        ext = get_extension(file.filename)
        content = await file.read()

        # ---------------- Parse file ----------------
        if ext == "pdf":
            text = parse_pdf(content)
            source_type = "pdf"

        elif ext == "json":
            text = parse_json(content)
            source_type = "json"

        elif ext in ["sql", "ddl"]:
            text = parse_sql(content)
            source_type = "sql"

        else:
            raise HTTPException(status_code=400, detail="Unsupported file type")

        # ---------------- Run AI ----------------
        result = analyze_document(text, source_type)

        # add runtime metadata
        result["timestamp"] = datetime.utcnow().isoformat()
        result["total_processing_ms"] = round((time.time() - start) * 1000, 2)

        RESULTS_DB[result["analysis_id"]] = result

        return {"analysis_id": result["analysis_id"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -----------------------------------------------------
# GET /api/v1/results/{id}
# -----------------------------------------------------
@app.get("/api/v1/results/{analysis_id}")
def results(analysis_id: str):
    if analysis_id not in RESULTS_DB:
        raise HTTPException(status_code=404, detail="Not found")

    return RESULTS_DB[analysis_id]


# -----------------------------------------------------
# GET /api/v1/domains
# -----------------------------------------------------
@app.get("/api/v1/domains")
def domains():
    base = Path(__file__).resolve().parent
    with open(base / "data" / "domains.json", "r") as f:
        return json.load(f)


# -----------------------------------------------------
# GET /api/v1/model/info
# -----------------------------------------------------
@app.get("/api/v1/model/info")
def model_info():
    return {
        "model_type": "zero-shot-classification",
        "model_name": "facebook/bart-large-mnli",
        "reasoning": "BART + keyword density calibration"
    }

