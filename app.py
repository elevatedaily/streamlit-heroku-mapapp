import streamlit as st
import pandas as pd
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

# Load the forecast data CSV
df = pd.read_csv('forecast_data1.csv')

df.rename(columns={
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'month': 'Month',
    'year': 'Year',
    'predicted_individuals': 'Individuals'
}, inplace=True)

# Sidebar Filters
st.sidebar.title("Filter")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
selected_month = st.sidebar.selectbox(
    "Select Month",
    options=list(range(1, 13)),
    format_func=lambda x: pd.to_datetime(f"2022-{x}-01").strftime("%B")
)

# Filter data
filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

st.title("Predicted Displacement Map")
st.subheader(f"{pd.to_datetime(f'{selected_year}-{selected_month}-01').strftime('%B %Y')}")

if filtered.empty:
    st.warning("No data available.")
else:
    vmin, vmax = filtered["Individuals"].min(), filtered["Individuals"].max()
    vmin, vmax = (vmin - 1, vmax + 1) if vmin == vmax else (vmin, vmax)
    colormap = cm.LinearColormap(["blue", "green", "yellow", "red"], vmin=vmin, vmax=vmax)
    colormap.caption = "Predicted Displacement"

    m = folium.Map(location=[15, 32], zoom_start=6)
    colormap.add_to(m)

    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            color=colormap(row["Individuals"]),
            fill=True,
            fill_color=colormap(row["Individuals"]),
            fill_opacity=0.7,
            popup=f"{row['Individuals']:.1f} displaced"
        ).add_to(m)

    st_folium(m, width=700, height=500)
