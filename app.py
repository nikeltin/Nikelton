import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static

# Load your data
df = pd.read_excel("nursing_homes_geocoded.xlsx")
df = df.dropna(subset=["Latitude", "Longitude", "Approved No of Beds"])
df["Approved No of Beds"] = pd.to_numeric(df["Approved No of Beds"], errors="coerce")

# Sidebar filters
bed_limit = st.slider("Max number of beds", 0, 100, 20)

# Filtered data
filtered_df = df[df["Approved No of Beds"] <= bed_limit]

# Create map
gk2_coords = [28.5411, 77.2342]
m = folium.Map(location=gk2_coords, zoom_start=12)
marker_cluster = MarkerCluster().add_to(m)

for _, row in filtered_df.iterrows():
    folium.Marker(
        location=[row["Latitude"], row["Longitude"]],
        popup=f"{row['Name']}<br>{row['Address']}<br>{int(row['Approved No of Beds'])} beds",
        tooltip=row["Name"]
    ).add_to(marker_cluster)

folium.Circle(location=gk2_coords, radius=5000, color="blue", fill=False).add_to(m)
folium.Circle(location=gk2_coords, radius=10000, color="blue", fill=False).add_to(m)
folium.Circle(location=gk2_coords, radius=20000, color="blue", fill=False).add_to(m)

# Render map
folium_static(m)
