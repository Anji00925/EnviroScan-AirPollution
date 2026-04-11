import requests
import logging
from typing import Optional, Dict, Any
from src.config import OPENWEATHER_API_KEY

def fetch_live_air_quality(lat: float, lon: float) -> Optional[Dict[str, Any]]:

   # Fetch live air pollution data from OpenWeather API for given coordinates.

    if not OPENWEATHER_API_KEY:
        logging.error("API Key missing. Cannot fetch live data.")
        return None

    url = (
        f"http://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_API_KEY}"
    )
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Check for 4xx and 5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching air quality data: {e}")
        return None


def parse_pollution_data(data: Dict[str, Any]) -> Optional[Dict[str, float]]:
    # \"\"\"
    # Extract essential component values from OpenWeather JSON response.
    # \"\"\"
    try:
        if not data or "list" not in data or len(data["list"]) == 0:
            return None

        item = data["list"][0]
        comp = item.get("components", {})
        main = item.get("main", {})

        return {
            "PM2.5": comp.get("pm2_5", 0.0),
            "NO2": comp.get("no2", 0.0),
            "CO": comp.get("co", 0.0),
            "O3": comp.get("o3", 0.0),
            "AQI": main.get("aqi", 0.0)
        }
    except Exception as e:
        logging.error(f"Error parsing pollution data: {e}")
        return None
