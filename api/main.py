from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI()

# Load artifacts
model = None
preprocessor = None

class EventInput(BaseModel):
    event_type: str
    state: str
    month: int
    season: str
    magnitude: float
    magnitude_type: str
    begin_lat: float
    begin_lon: float

@app.on_event("startup")
def load_artifacts():
    global model, preprocessor
    model = load("models/storm_damage_model.joblib")
    preprocessor = load("data/interim/feature_preprocessor.joblib")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict(data: EventInput):
    input_dict = data.dict()
    df = pd.DataFrame([input_dict])

    # Apply preprocessing (OneHotEncoder + Imputation)
    X = preprocessor.transform(df)

    pred = model.predict(X)[0]
    return {"predicted_damage": float(pred)}
