import pandas as pd
import logging
from typing import Optional
from src.config import DATA_PATH
import streamlit as st
import datetime

@st.cache_data
def load_data() -> pd.DataFrame:
    
    try:
        df = pd.read_csv(DATA_PATH)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"])
        logging.info("Historical data loaded successfully.")
        return df
    except Exception as e:
        logging.error(f"Failed to load historical data from {DATA_PATH}: {e}")
        return pd.DataFrame()

def apply_filters(
    df: pd.DataFrame, 
    country: str, 
    city: str, 
    source: str, 
    start_date: datetime.date, 
    end_date: datetime.date
) -> pd.DataFrame:
    
    filtered_df = df.copy()

    if country != "All":
        filtered_df = filtered_df[filtered_df["Country"] == country]
    if city != "All":
        filtered_df = filtered_df[filtered_df["City"] == city]
    if source != "All":
        filtered_df = filtered_df[filtered_df["pollution_source"] == source]

    # Date range filtering
    filtered_df = filtered_df[
        (filtered_df["Timestamp"].dt.date >= start_date) &
        (filtered_df["Timestamp"].dt.date <= end_date)
    ]
    return filtered_df

def get_alert_level(aqi: float) -> str:
    
    if aqi > 200:
        return "CRITICAL"
    elif aqi > 100:
        return "WARNING"
    return "SAFE"

def evaluate_alerts(df: pd.DataFrame) -> pd.DataFrame:
    
    if "AQI Value" in df.columns:
        df["Alert"] = df["AQI Value"].apply(get_alert_level)
    return df
