import os
from dotenv import load_dotenv
import logging
import streamlit as st

# Initialize logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Load environment variables (Local)
load_dotenv()

# Configuration Settings
# For Streamlit Cloud, st.secrets natively reads the server console settings
try:
    OPENWEATHER_API_KEY = st.secrets.get("OPENWEATHER_API_KEY")
    if not OPENWEATHER_API_KEY:
        OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
except Exception:
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    logging.warning("OPENWEATHER_API_KEY is not set in the environment variables.")

DATA_PATH = "enviroscan_week3_labeled_dataset.csv"
MODEL_PATH = "pollution_source_model.pkl"
