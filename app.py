import folium
import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

# Page configuration
st.set_page_config(
    page_title="Agartala Traffic & Livelihood Intelligence",
    page_icon="■",
    layout="wide",
)

# Professional Dark Mode Styling
st.markdown(
    """
    <style>
        .stApp {
            background-color: #0d1117;
            color: #c9d1d9;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        .dashboard-title {
            font-size: 2.2rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.1rem;
        }
        .dashboard-subtitle {
            font-size: 0.95rem;
            color: #8b949e;
            margin-bottom: 1.5rem;
        }
        .card-header {
            font-size: 1.15rem;
            font-weight: 600;
            color: #ffffff;
            margin-bottom: 0.75rem;
            border-left: 3px solid #58a6ff;
            padding-left: 8px;
        }
        .disruption-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-left: 3px solid #f85149;
            padding: 12px 14px;
            margin-bottom: 10px;
            border-radius: 6px;
        }
        .node-name {
            font-weight: 600;
            font-size: 0.95rem;
            color: #ffffff;
        }
        .node-meta {
            font-size: 0.83rem;
            color: #8b949e;
            margin-top: 3px;
        }
        
        /* Impact & Solution Custom Card Styling */
        .impact-card {
            background: #161b22;
            border: 1px solid #30363d;
            border-radius: 8px;
            padding: 18px;
            margin-bottom: 15px;
        }
        .impact-card-title {
            font-size: 1.05rem;
            font-weight: 600;
            color: #f0f6fc;
            margin-bottom: 6px;
        }
        .impact-card-body {
            font-size: 0.88rem;
            color: #8b949e;
            line-height: 1.5;
        }
        .solution-tag {
            display: inline-block;
            background: #1f6feb22;
            color: #58a6ff;
            border: 1px solid #1f6feb;
            padding: 2px 8px;
            font-size: 0.75rem;
            font-weight: 600;
            border-radius: 4px;
            margin-bottom: 8px;
        }
        
        [data-testid="stMetricValue"] {
            color: #ffffff !important;
            font-weight: 700;
        }
        [data-testid="stMetricLabel"] {
            color: #8b949e !important;
        }
        [data-testid="stSidebar"] {
            background-color: #010409;
            border-right: 1px solid #30363d;
        }
        [data-testid="stSidebar"] label {
            color: #c9d1d9 !important;
            font-weight: 600;
        }
    </style>
""",
    unsafe_allow_html=True,
)


# Load dataset
@st.cache_data
def load_data():
  return pd.read_csv("agartala_traffic_impact_expanded.csv")


df = load_data()

# App Header
st.markdown(
    '<div class="dashboard-title">Agartala Traffic & Livelihood'
    " Intelligence</div>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="dashboard-subtitle">Longitudinal analytics tracking urban'
    " congestion growth (2015–2026) and its cascading effects on community"
    " peace, air quality, and economic productivity.</div>",
    unsafe_allow_html=True,
)

# Sidebar Controls
st.sidebar.markdown("### Controls")
selected_year = st.sidebar.slider(
    "Timeline Year", int(df["Year"].min()), int(df["Year"].max()), 2026
)

zone_types = df["Zone_Type"].unique()
selected_zones = st.sidebar.multiselect(
    "Zone Classification", zone_types, default=zone_types
)

# Filter dataframe
filtered_df = df[
    (df["Year"] == selected_year) & (df["Zone_Type"].isin(selected_zones))
]

# Top KPI Metric Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("Selected Period", selected_year)
c2.metric(
    "Mean Congestion Index",
    f"{filtered_df['Congestion_Index'].mean():.2f} / 10",
)
c3.metric(
    "Avg Commute Delay",
    f"{int(filtered_df['Daily_Commute_Delay_mins'].mean())} mins",
)
c4.metric(
    "Mean Economic Drain",
    f"₹{filtered_df['Economic_Loss_INR_Lakhs'].mean():.1f} Lakhs",
)

st.markdown(
    "<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid"
    " #30363d;'>",
    unsafe_allow_html=True,
)

# Layout Split: Map on left, Insights on right
map_column, info_column = st.columns([2, 1])

with map_column:
  st.markdown(
      f'<div class="card-header">Geospatial Distribution ({selected_year})</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      '<p style="font-size: 0.85rem; color: #8b949e; margin-bottom: 0.75rem;">Hover'
      " or click on any node to review localized livelihood and peace impact"
      " metrics.</p>",
      unsafe_allow_html=True,
  )

  # Using standard OpenStreetMap tiles (100% free, no API key required)
  m = folium.Map(
      location=[23.8315, 91.2868], zoom_start=13, tiles="OpenStreetMap"
  )

  for _, row in filtered_df.iterrows():
    color = (
        "#f85149"
        if row["Congestion_Index"] > 7.5
        else "#db6d28"
        if row["Congestion_Index"] > 5.0
        else "#2ea043"
    )

    popup_html = f"""
        <div style="font-family: -apple-system, BlinkMacSystemFont, sans-serif; width: 220px; font-size: 12px; color: #111111; background: #ffffff; padding: 10px; border-radius: 6px;">
            <div style="font-weight: 700; font-size: 13px; margin-bottom: 3px; color: #111111;">{row['Area_Name']}</div>
            <div style="color: #666666; font-size: 11px; margin-bottom: 6px;">{row['Zone_Type']}</div>
            <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 4px 0;">
            <b>Congestion Index:</b> {row['Congestion_Index']}/10<br>
            <b>Growth vs 2015:</b> <span style="color:#f85149; font-weight:700;">+{row['Congestion_Growth_Pct']}%</span><br>
            <b>Peak Speed:</b> {row['Avg_Speed_kmph']} km/h<br>
            <b>Commute Delay:</b> +{row['Daily_Commute_Delay_mins']} mins<br>
            <b>Noise Pollution:</b> {row['Noise_Level_dB']} dB<br>
            <b>Air Quality Index:</b> {row['AQI_PM2_5']}<br>
            <b>Peace Stress Index:</b> {row['Peace_Stress_Index']}/10<br>
            <b>Economic Loss:</b> ₹{row['Economic_Loss_INR_Lakhs']} Lakhs/yr<br>
            <b>Ambulance Delay:</b> +{row['Ambulance_Delay_mins']} mins
        </div>
        """

    folium.CircleMarker(
        location=[row["Latitude"], row["Longitude"]],
        radius=5 + (row["Congestion_Index"] * 1.1),
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.9,
        weight=1,
        popup=folium.Popup(popup_html, max_width=240),
        tooltip=f"{row['Area_Name']} (Index: {row['Congestion_Index']})",
    ).add_to(m)

  st_folium(m, width=700, height=460)

with info_column:
  st.markdown(
      '<div class="card-header">Critical Disruption Nodes</div>',
      unsafe_allow_html=True,
  )
  st.markdown(
      f'<p style="font-size: 0.85rem; color: #8b949e; margin-bottom: 0.75rem;">Highest'
      f" stress zones in {selected_year}:</p>",
      unsafe_allow_html=True,
  )

  top_congested = filtered_df.sort_values(
      by="Congestion_Index", ascending=False
  ).head(5)
  for _, row in top_congested.iterrows():
    st.markdown(
        f"""
        <div class="disruption-card">
            <div class="node-name">{row['Area_Name']}</div>
            <div class="node-meta">
                Congestion: <b>{row['Congestion_Index']}</b> | Stress Index: <b>{row['Peace_Stress_Index']}</b>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Middle Section: Longitudinal Trends
st.markdown(
    "<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #30363d;'>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="card-header">Longitudinal Urban Degradation Trend'
    " (2015–2026)</div>",
    unsafe_allow_html=True,
)
trend_data = (
    df.groupby("Year")[
        ["Congestion_Index", "Noise_Level_dB", "Peace_Stress_Index"]
    ]
    .mean()
    .reset_index()
)
st.line_chart(
    trend_data.set_index("Year"), color=["#58a6ff", "#8b949e", "#f85149"]
)

# New Section: Societal & Environmental Impact & Future Recommendations
st.markdown(
    "<hr style='margin: 1.5rem 0; border: none; border-top: 1px solid #30363d;'>",
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="card-header">Societal Impact & Urban Resilience Planning</div>',
    unsafe_allow_html=True,
)

tab_impact, tab_solutions = st.tabs(
    ["Environmental & Citizen Impact", "Future Planning Recommendations"]
)

with tab_impact:
  col_a, col_b = st.columns(2)

  with col_a:
    st.markdown(
        """
        <div class="impact-card">
            <div class="impact-card-title">Impact on Citizen Wellbeing & Health</div>
            <div class="impact-card-body">
                • <b>Mental Stress & Peace:</b> Prolonged gridlocks at commercial hubs like Battala and Motorstand have elevated the average Peace Stress Index from 3.2 in 2015 to nearly 8.0 in 2026.<br>
                • <b>Emergency Response Vulnerability:</b> Critical transit corridors surrounding GB Hospital experience ambulance delay surges of up to +18 minutes during peak hours, creating severe health safety risks.<br>
                • <b>Productivity Drain:</b> Daily commuter delays averaging over 35–45 minutes per citizen accumulate millions in lost working hours each year across the local economy.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_b:
    st.markdown(
        """
        <div class="impact-card">
            <div class="impact-card-title">Impact on Atmosphere & Local Nature</div>
            <div class="impact-card-body">
                • <b>Air Quality Degradation:</b> Idling vehicles along major arterial roads contribute directly to elevated PM2.5 and AQI levels exceeding national safety limits during peak winter months.<br>
                • <b>Acoustic Pollution:</b> Ambient noise levels near major junctions consistently cross 78 dB, disturbing urban ecology and peaceful residential zones.<br>
                • <b>Fuel Waste & Carbon Footprint:</b> Excess stop-and-go driving causes thousands of liters of fuel to be wasted daily, worsening Agartala's microclimate heat retention.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with tab_solutions:
  col_1, col_2, col_3 = st.columns(3)

  with col_1:
    st.markdown(
        """
        <div class="impact-card">
            <span class="solution-tag">INFRASTRUCTURE</span>
            <div class="impact-card-title">Intelligent Traffic Management</div>
            <div class="impact-card-body">
                Deploy dynamic, AI-powered traffic signals at top-congested intersections (Motorstand, Battala) that adjust green-light timing based on real-time vehicle density to reduce idle times by up to 25%.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_2:
    st.markdown(
        """
        <div class="impact-card">
            <span class="solution-tag">TRANSIT & LOGISTICS</span>
            <div class="impact-card-title">Outer Ring Bypass & Dedicated Lanes</div>
            <div class="impact-card-body">
                Reroute heavy commercial freight vehicles around the city core via an expanded NH-8 bypass loop, and introduce dedicated emergency vehicle lanes near medical zones like GB Hospital.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

  with col_3:
    st.markdown(
        """
        <div class="impact-card">
            <span class="solution-tag">ENVIRONMENT & URBAN DESIGN</span>
            <div class="impact-card-title">Green Buffers & Clean Mobility</div>
            <div class="impact-card-body">
                Plant high-density green acoustic buffers along heavy traffic corridors to absorb sound waves and filter PM2.5, alongside expanding electric auto-rickshaw charging networks.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )