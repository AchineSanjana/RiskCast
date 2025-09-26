from fastapi import FastAPI
from pydantic import BaseModel
from joblib import load
import pandas as pd

app = FastAPI(title='Storm Damage Predictor API')
model = None

class StormEvent(BaseModel):
    event_type: str
    state: str
    month: int
    season: str
    magnitude: float | None = None
    magnitude_type: str | None = None
    begin_lat: float | None = None
    begin_lon: float | None = None

@app.on_event('startup')
def load_model():
    global model
    model = load('models/storm_damage_model.joblib')

@app.get('/health')
def health():
    return {'status': 'ok'}

@app.post('/predict')
def predict(e: StormEvent):
    assert model is not None, 'Model not loaded'
    X = pd.DataFrame([e.dict()])
    y = model.predict(X)[0]
    return {'predicted_damage_property': float(y)}
