# FDM Storm Damage Predictor — Project Skeleton

This repository is a starting point for your Fundamentals of Data Mining mini project.
It includes a clean folder layout, starter code, and step-by-step commands.

## 1) Prereqs
- Install Python 3.10 or newer
- Install Git
- (Recommended) Visual Studio Code + Python & Jupyter extensions

## 2) Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 3) Install dependencies
```bash
pip install -U pip
pip install -r requirements.txt
```

## 4) Put your dataset
Place your CSV(s) into `data/raw/` (e.g., `StormEvents_details-ftp_v1.0_d2010_*.csv`).

## 5) Open the starter notebook
```bash
jupyter notebook notebooks/01_eda.ipynb
```

## 6) Run the API (after training a model)
```bash
uvicorn api.main:app --reload
```

## 7) Run the Streamlit app
```bash
streamlit run app/ui.py
```
