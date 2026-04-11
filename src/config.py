import os
from dotenv import load_dotenv
import logging

# Initialize logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(module)s: %(message)s",
    handlers=[logging.StreamHandler()]
)

# Load environment variables
load_dotenv()

# Configuration Settings
OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not OPENWEATHER_API_KEY:
    logging.warning("OPENWEATHER_API_KEY is not set in the environment variables.")

DATA_PATH = "enviroscan_week3_labeled_dataset.csv"
MODEL_PATH = "pollution_source_model.pkl"
