import streamlit as st
import datetime

# =======================
# APP CONFIGURATION
# =======================
st.set_page_config(page_title="EnviroScan Dashboard", layout="wide")

# Local module imports
from src.config import logging
from src.api import fetch_live_air_quality, parse_pollution_data
from src.ml_model import load_model, live_to_model_input, predict_source
from src.data_processing import load_data, apply_filters, evaluate_alerts
from src.components import render_alert_banner, render_metrics, render_charts, render_map
st.title("🌍 EnviroScan – AI Pollution Monitoring Dashboard")

def main():
    logging.info("Streamlit app fully initialized and running.")
    
    # Initialize Core Application Modules
    model = load_model()
    df = load_data()

    if df.empty:
        st.error("Historical dataset failed to load. Please check `enviroscan_week3_labeled_dataset.csv` in the current directory.")
        return

    # =======================
    # SIDEBAR - LIVE DATA
    # =======================
    st.sidebar.header("🔍 Filters & Tools")
    st.sidebar.subheader("🌐 Live Pollution (API)")

    lat = st.sidebar.number_input("Latitude", value=17.3850, format="%.4f")
    lon = st.sidebar.number_input("Longitude", value=78.4867, format="%.4f")

    if st.sidebar.button("Fetch Live Pollution"):
        with st.spinner("Fetching data from OpenWeatherAPI..."):
            live_data = fetch_live_air_quality(lat, lon)
            if live_data:
                parsed = parse_pollution_data(live_data)
                
                # Show fetched data overview
                st.subheader("📡 Live Pollution Data Overview")
                st.json(parsed)

                # Process the ML prediction
                if model and parsed:
                    input_df = live_to_model_input(parsed, lat, lon)
                    prediction, confidence = predict_source(model, input_df)

                    st.subheader("🤖 Predicted Pollution Source")
                    st.success(f"**{prediction}** ({confidence:.2f}% confidence)")
            else:
                st.sidebar.error("Failed to fetch live data (check logs/API keys)")

    st.sidebar.divider()

    # =======================
    # SIDEBAR - HISTORICAL DATA FILTERS
    # =======================
    st.sidebar.subheader("📅 Historical Data Filtering")
    
    country_opts = ["All"] + sorted(df["Country"].unique().tolist())
    selected_country = st.sidebar.selectbox("Country", country_opts)
    
    city_opts = ["All"] + sorted(df["City"].unique().tolist())
    selected_city = st.sidebar.selectbox("City", city_opts)
    
    source_opts = ["All"] + sorted(df["pollution_source"].unique().tolist())
    selected_source = st.sidebar.selectbox("Pollution Source", source_opts)

    min_date = df["Timestamp"].min().date()
    max_date = df["Timestamp"].max().date()

    start_date, end_date = st.sidebar.date_input(
        "Date Range", 
        [min_date, max_date], 
        min_value=min_date, 
        max_value=max_date
    )

    # Apply processing
    filtered_df = apply_filters(df, selected_country, selected_city, selected_source, start_date, end_date)
    filtered_df = evaluate_alerts(filtered_df)

    # Render Dashboard UI via Components
    render_alert_banner(filtered_df)
    render_metrics(filtered_df)
    render_charts(filtered_df)
    render_map(filtered_df)

    # =======================
    # EXPORT DATA
    # =======================
    st.sidebar.divider()
    st.sidebar.subheader("⬇️ Download Current View")
    st.sidebar.download_button(
        label="Download Filtered CSV",
        data=filtered_df.to_csv(index=False),
        file_name="pollution_report.csv",
        mime="text/csv"
    )

if __name__ == "__main__":
    main()
