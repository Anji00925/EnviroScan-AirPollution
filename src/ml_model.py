import joblib
import pandas as pd
import logging
from typing import Any, Tuple
from src.config import MODEL_PATH
import streamlit as st

@st.cache_resource
def load_model() -> Any:
    #\"\"\"
    # Load the trained machine learning model from disk.
    # Cached explicitly for Streamlit efficiency.
    #\"\"\"
    try:
        model = joblib.load(MODEL_PATH)
        logging.info("ML Model loaded successfully.")
        return model
    except Exception as e:
        logging.error(f"Failed to load ML model from {MODEL_PATH}: {e}")
        return None

def live_to_model_input(parsed_data: dict, lat: float, lon: float) -> pd.DataFrame:
    # \"\"\"
    # Convert parsed real-time API data into a Pandas DataFrame formatted for the ML Model.
    # \"\"\"
    return pd.DataFrame([{
        "AQI Value": parsed_data.get("AQI", 0) * 50,  # Scaled based on original app logic
        "NO2 AQI Value": parsed_data.get("NO2", 0),
        "PM2.5 AQI Value": parsed_data.get("PM2.5", 0),
        "Temperature (C)": 25,  # Standard fallback or fetch real
        "Humidity (%)": 60,     # Standard fallback or fetch real
        "Wind Speed (m/s)": 3,  # Standard fallback or fetch real
        "Latitude": lat,
        "Longitude": lon
    }])

def predict_source(model: Any, input_df: pd.DataFrame) -> Tuple[str, float]:
    # \"\"\"
    # Predict the pollution source using the ML model.
    # \"\"\"
    try:
        prediction = model.predict(input_df)[0]
        confidence = max(model.predict_proba(input_df)[0]) * 100
        return prediction, confidence
    except Exception as e:
        logging.error(f"Model prediction failed: {e}")
        return "Unknown", 0.0
