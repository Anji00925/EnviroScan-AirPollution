import streamlit as st
import pandas as pd
import folium
from folium.plugins import HeatMap
import matplotlib.pyplot as plt

def render_alert_banner(filtered_df: pd.DataFrame) -> None:
    # \"\"\"
    # Render the real-time alerts at the dashboard top.
    # \"\"\"
    st.subheader("🚨 Pollution Alerts")

    if (filtered_df["Alert"] == "CRITICAL").any():
        st.error("🚨 CRITICAL pollution detected in filtered locations")
    elif (filtered_df["Alert"] == "WARNING").any():
        st.warning("⚠️ Elevated pollution detected in some selected locations")
    else:
        st.success("✅ Pollution levels are safe for the selected filters")

def render_metrics(filtered_df: pd.DataFrame) -> None:
    # \"\"\"
    # Render top-level metrics.
    # \"\"\"
    st.subheader("📊 Dataset Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Records", filtered_df.shape[0])
    c2.metric("Countries", filtered_df["Country"].nunique())
    c3.metric("Cities", filtered_df["City"].nunique())

def render_charts(filtered_df: pd.DataFrame) -> None:
    # \"\"\"
    # Render AQI trends and source distribution charts.
    # \"\"\"
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 AQI Trend (Hourly Average)")
        trend = filtered_df.groupby(filtered_df["Timestamp"].dt.hour)["AQI Value"].mean()
        st.line_chart(trend)

    with col2:
        st.subheader("🧪 Source Distribution")
        fig, ax = plt.subplots(figsize=(4, 4))
        source_counts = filtered_df["pollution_source"].value_counts()
        ax.pie(
            source_counts,
            labels=source_counts.index,
            autopct="%1.1f%%"
        )
        st.pyplot(fig)

def render_map(filtered_df: pd.DataFrame) -> None:
    # \"\"\"
    # Render the Folium heatmap and markers.
    # \"\"\"
    st.subheader("🗺️ Pollution Map")

    if not filtered_df.empty:
        # Sample data to avoid browser performance issues natively in folium
        map_df = filtered_df.sample(min(1000, len(filtered_df)), random_state=42)
        m = folium.Map(
            location=[map_df["Latitude"].mean(), map_df["Longitude"].mean()],
            zoom_start=2
        )

        colors = {
            "Industrial": "red",
            "Vehicular": "blue",
            "Agricultural": "green",
            "Residential": "purple",
            "Natural": "gray"
        }

        for _, r in map_df.iterrows():
            folium.CircleMarker(
                [r["Latitude"], r["Longitude"]],
                radius=4,
                color=colors.get(r["pollution_source"], "black"),
                popup=f"{r['City']} | AQI: {r['AQI Value']:.1f}",
                fill=True,
                fill_opacity=0.7
            ).add_to(m)

        HeatMap(
            map_df[["Latitude", "Longitude", "AQI Value"]].values.tolist(),
            radius=15
        ).add_to(m)

        st.components.v1.html(m._repr_html_(), height=600)
    else:
        st.warning("No data available for the selected filters.")
