import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.stats import ttest_ind
import os

# ---------- 1. THEME & HELPERS ----------
CHART_BG  = '#0d1117'
CHART_FG  = '#e2b96f'
GRID_COL  = '#2a2a3f'

sns.set_theme(style='darkgrid')
plt.rcParams.update({
    'text.color': CHART_FG, 'axes.labelcolor': CHART_FG,
    'xtick.color': CHART_FG, 'ytick.color': CHART_FG,
    'axes.titlecolor': CHART_FG, 'figure.facecolor': CHART_BG,
    'axes.facecolor': CHART_BG, 'axes.edgecolor': CHART_FG,
    'grid.color': GRID_COL, 'font.size': 10, 'savefig.facecolor': CHART_BG,
})

def styled_fig(w=6, h=3.5):
    fig, ax = plt.subplots(figsize=(w, h))
    fig.patch.set_edgecolor(CHART_FG)
    fig.patch.set_linewidth(1.5)
    return fig, ax

def inr(num):
    try:
        num = int(round(float(num)))
        s = str(abs(num))
        if len(s) <= 3: return f"₹{s}"
        last3 = s[-3:]; rest = s[:-3]; parts = []
        while len(rest) > 2:
            parts.append(rest[-2:]); rest = rest[:-2]
        if rest: parts.append(rest)
        parts.reverse()
        return f"₹{','.join(parts)},{last3}"
    except: return "₹0"

def indian_num(num):
    try:
        s = str(abs(int(num)))
        if len(s) <= 3: return s
        last3 = s[-3:]; rest = s[:-3]; parts = []
        while len(rest) > 2:
            parts.append(rest[-2:]); rest = rest[:-2]
        if rest: parts.append(rest)
        parts.reverse()
        return ','.join(parts) + ',' + last3
    except: return "0"

def metric_card(value, label):
    return f'<div class="metric-card"><h2>{value}</h2><p>{label}</p></div>'

# BANGALORE COORDINATES LOOKUP (For the 50 areas in your data)
COORDS = {
    'Tumkur Road': [13.0425, 77.4935], 'Magadi Road': [12.9754, 77.4851], 'Sahakar Nagar': [13.0624, 77.5907],
    'HSR Layout': [12.9121, 77.6446], 'Rajajinagar': [12.9893, 77.5533], 'Kadugodi': [12.9984, 77.7609],
    'Bannerghatta Road': [12.8907, 77.5954], 'Chamarajpet': [12.9605, 77.5658], 'RT Nagar': [13.0247, 77.5948],
    'Hosur Road': [12.9118, 77.6322], 'Kammanahalli': [13.0159, 77.6373], 'Cox Town': [12.9972, 77.6186],
    'Indiranagar': [12.9784, 77.6408], 'Ramamurthy Nagar': [13.0120, 77.6777], 'Electronic City': [12.8452, 77.6632],
    'Koramangala': [12.9352, 77.6245], 'Basavanagudi': [12.9406, 77.5738], 'Padmanabhanagar': [12.9184, 77.5583],
    'Mysore Road': [12.9554, 77.5273], 'Yelahanka': [13.1007, 77.5963], 'Frazer Town': [12.9968, 77.6111],
    'Jayanagar': [12.9308, 77.5830], 'Majestic': [12.9767, 77.5713], 'Yeshwanthpur': [13.0235, 77.5550],
    'Peenya': [13.0329, 77.5273], 'Marathahalli': [12.9569, 77.7011], 'KR Puram': [13.0117, 77.7033],
    'Hulimavu': [12.8790, 77.6033], 'Shivajinagar': [12.9857, 77.5977], 'Hennur': [13.0258, 77.6311],
    'Devanahalli': [13.2484, 77.7126], 'Rajarajeshwari Nagar': [12.9126, 77.5222], 'Ulsoor': [12.9817, 77.6286],
    'Shantinagar': [12.9575, 77.5983], 'JP Nagar': [12.9063, 77.5857], 'Chickpet': [12.9700, 77.5780],
    'Langford Town': [12.9575, 77.6074], 'BTM Layout': [12.9165, 77.6101], 'Sarjapur Road': [12.9184, 77.6705],
    'Bellandur': [12.9304, 77.6784], 'Richmond Town': [12.9667, 77.6000], 'Kengeri': [12.9176, 77.4837],
    'Banashankari': [12.9254, 77.5468], 'Vijayanagar': [12.9640, 77.5350], 'Malleshwaram': [12.9984, 77.5719],
    'Whitefield': [12.9698, 77.7500], 'MG Road': [12.9733, 77.6033], 'Hebbal': [13.0358, 77.5970],
    'Nagarbhavi': [12.9719, 77.5128], 'Varthur': [12.9406, 77.7469]
}

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.drop(columns=['Vehicle Images', 'Unnamed: 20'], inplace=True, errors='ignore')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = df['Date'].dt.hour
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce').fillna(0)
    df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce').fillna(0)
    
    # Map coordinates for the map visual
    df['lat'] = df['Pickup_Location'].map(lambda x: COORDS.get(x, [None, None])[0])
    df['lon'] = df['Pickup_Location'].map(lambda x: COORDS.get(x, [None, None])[1])
    return df

# ---------- 2. PAGE CONFIG & CSS ----------
st.set_page_config(page_title="Ola Ride Analytics", page_icon="🚖", layout="wide")

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
        padding: 1.2rem; border-radius: 12px; color: white; text-align: center;
        box-shadow: 2px 4px 10px rgba(0,0,0,0.3); border: 1px solid #2a2a3f; margin-bottom: 10px;
    }
    .metric-card h2 { margin: 0; font-size: 1.8rem; color: #e2b96f; }
    .metric-card p { margin: 0; font-size: 0.85rem; color: #cbd5e0; }
    .section-header {
        font-size: 1rem; font-weight: 600; color: #cbd5e0; margin: 1.2rem 0 0.5rem;
        border-left: 4px solid #e2b96f; padding: 0.4rem 0.6rem; background: #16213e;
    }
</style>
""", unsafe_allow_html=True)

# ---------- 3. DATA LOADING ----------
DATA_PATH = "Bookings.csv"
if os.path.exists(DATA_PATH):
    df_raw = load_data(DATA_PATH)
else:
    st.error("Bookings.csv not found!")
    st.stop()

# Sidebar
v_type = st.sidebar.multiselect("Vehicle Type", sorted(df_raw['Vehicle_Type'].unique()), default=sorted(df_raw['Vehicle_Type'].unique()))
df = df_raw[df_raw['Vehicle_Type'].isin(v_type)].copy()
successful = df[df['Booking_Status'] == 'Success'].copy()

# ---------- 4. DASHBOARD ----------
st.title("Ola Ride Analytics 🚖")

# KPI ROW
c1, c2, c3, c4 = st.columns(4)
c1.markdown(metric_card(indian_num(len(df)), "Total Bookings"), unsafe_allow_html=True)
c2.markdown(metric_card(f"{(len(successful)/len(df)*100):.1f}%" if len(df)>0 else "0%", "Success Rate"), unsafe_allow_html=True)
c3.markdown(metric_card(inr(successful['Booking_Value'].sum()), "Total Revenue"), unsafe_allow_html=True)
c4.markdown(metric_card(inr(successful['Booking_Value'].mean()) if len(successful)>0 else "₹0", "Avg Ride Value"), unsafe_allow_html=True)

# ROW 1: STATUS & REVENUE
col1, col2 = st.columns(2)
with col1:
    st.markdown('<p class="section-header">Booking Status Breakdown</p>', unsafe_allow_html=True)
    counts = df['Booking_Status'].value_counts()
    fig, ax = styled_fig()
    sns.barplot(x=counts.values, y=counts.index, palette='viridis', ax=ax)
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown('<p class="section-header">Revenue by Vehicle</p>', unsafe_allow_html=True)
    rev = successful.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values()
    fig, ax = styled_fig()
    rev.plot(kind='barh', ax=ax, color='#e2b96f')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
    st.pyplot(fig)
    plt.close()

# NEW ROW: GEOGRAPHIC MAP
st.markdown('<p class="section-header">Ride Hotspots (Pickup Locations)</p>', unsafe_allow_html=True)
map_df = df.dropna(subset=['lat', 'lon'])
if not map_df.empty:
    st.map(map_df[['lat', 'lon']], color='#e2b96f', size=20)
else:
    st.warning("Coordinate mapping failed for the locations.")

# ROW: STATISTICAL BOXPLOT (FIXED)
st.markdown('<p class="section-header">Peak vs Off-Peak Distance Analysis</p>', unsafe_allow_html=True)
df['Period'] = df['Hour'].apply(lambda h: 'Peak (17-21)' if 17 <= h <= 21 else 'Off-Peak')
col_s, col_p = st.columns([1, 2])

with col_s:
    p_data = df[df['Period'] == 'Peak (17-21)']['Ride_Distance'].dropna()
    o_data = df[df['Period'] == 'Off-Peak']['Ride_Distance'].dropna()
    if len(p_data) > 1 and len(o_data) > 1:
        t, p_val = ttest_ind(p_data, o_data, equal_var=False)
        st.info(f"P-Value: {p_val:.4f}\n\nConclusion: {'Significant' if p_val < 0.05 else 'Not Significant'}")

with col_p:
    fig, ax = styled_fig(8, 4)
    sns.boxplot(data=df, x='Period', y='Ride_Distance', ax=ax, order=['Off-Peak', 'Peak (17-21)'], palette=['#3498db', '#e74c3c'])
    st.pyplot(fig)
    plt.close()

st.markdown("---")
st.markdown("<p style='text-align:center; color:gray;'>MBA Data Portfolio</p>", unsafe_allow_html=True)
