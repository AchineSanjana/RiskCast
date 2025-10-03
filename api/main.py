from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI()

# Load trained pipeline model (preprocessor + regressor)
model = None

@app.on_event("startup")
def load_artifacts():
    global model
    model = load("models/storm_damage_model.joblib")  # Pipeline (preprocessor + model)

@app.get("/health")
def health():
    return {"status": "ok"}

import numpy as np

@app.post("/predict")
def predict(data: dict):
    try:
        # Convert keys to uppercase for model input
        input_dict = {k.upper(): v for k, v in data.items()}
        df = pd.DataFrame([input_dict])

        # Run prediction
        pred = model.predict(df)[0]

        # Handle both single-output and multi-output
        if isinstance(pred, (list, np.ndarray)) and len(pred) == 2:
            property_damage = max(0.0(float(pred[0])))
            crop_damage = max(0.0(float(pred[1])))
        else:
            property_damage = float(pred)
            crop_damage = 0.0

        total_damage = property_damage + crop_damage

        return {
            "property_damage": property_damage,
            "crop_damage": crop_damage,
            "total_damage": total_damage
        }

    except Exception as e:
        import traceback
        traceback.print_exc()

        # Always return the expected keys, with fallback values
        return {
            "property_damage": 0.0,
            "crop_damage": 0.0,
            "total_damage": 0.0,
            "error": str(e)
        }

