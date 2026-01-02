import requests

API_KEY = "e79fb67e829144c66828471ab9d07dd9"

def fetch_live_air_quality(lat, lon):
    url = (
        "http://api.openweathermap.org/data/2.5/air_pollution"
        f"?lat={lat}&lon={lon}&appid={API_KEY}"
    )
    response = requests.get(url)
    data = response.json()
    return data

def parse_pollution_data(data):
    comp = data["list"][0]["components"]
    return {
        "PM2.5 AQI Value": comp["pm2_5"],
        "NO2 AQI Value": comp["no2"],
        "AQI Value": data["list"][0]["main"]["aqi"]
    }


def predict_source(model, input_df):
    return model.predict(input_df)[0]

