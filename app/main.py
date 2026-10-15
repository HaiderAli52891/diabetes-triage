import json
from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

ART = Path(__file__).resolve().parent.parent / "artifacts"
model = joblib.load(ART / "model.joblib")
VERSION = json.loads((ART / "metrics.json").read_text())["model_version"]

class Patient(BaseModel):
    model_config = ConfigDict(extra="forbid")
    age: float; sex: float; bmi: float; bp: float
    s1: float; s2: float; s3: float; s4: float; s5: float; s6: float

app = FastAPI(title="Diabetes Triage")

@app.get("/health")
def health():
    return {"status": "ok", "model_version": VERSION}

@app.post("/predict")
def predict(p: Patient):
    X = pd.DataFrame([p.model_dump()])
    return {"prediction": float(model.predict(X)[0])}