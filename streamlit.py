import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns
from scipy.stats import ttest_ind
import os

# ---------- GLOBAL THEME & HELPERS ----------
CHART_BG  = '#0d1117'
CHART_FG  = '#e2b96f'
GRID_COL  = '#2a2a3f'

sns.set_theme(style='darkgrid')
plt.rcParams.update({
    'text.color':        CHART_FG,
    'axes.labelcolor':   CHART_FG,
    'xtick.color':       CHART_FG,
    'ytick.color':       CHART_FG,
    'axes.titlecolor':   CHART_FG,
    'figure.facecolor':  CHART_BG,
    'axes.facecolor':    CHART_BG,
    'axes.edgecolor':    CHART_FG,
    'grid.color':        GRID_COL,
    'font.size':         10,
    'savefig.facecolor': CHART_BG,
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
        if len(s) <= 3:
            return f"₹{s}"
        last3 = s[-3:]; rest = s[:-3]; parts = []
        while len(rest) > 2:
            parts.append(rest[-2:]); rest = rest[:-2]
        if rest: parts.append(rest)
        parts.reverse()
        return f"₹{','.join(parts)},{last3}"
    except:
        return f"₹0"

def indian_num(num):
    s = str(abs(int(num)))
    if len(s) <= 3:
        return s
    last3 = s[-3:]; rest = s[:-3]; parts = []
    while len(rest) > 2:
        parts.append(rest[-2:]); rest = rest[:-2]
    if rest: parts.append(rest)
    parts.reverse()
    return ','.join(parts) + ',' + last3

# FIX: Added missing metric_card function
def metric_card(value, label):
    return f'''
    <div class="metric-card">
        <h2>{value}</h2>
        <p>{label}</p>
    </div>
    '''

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    # Basic cleaning
    df.drop(columns=['Vehicle Images', 'Unnamed: 20'], inplace=True, errors='ignore')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = df['Date'].dt.hour
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce').fillna(0)
    df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce').fillna(0)
    return df

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Ola Ride Analytics", page_icon="🚖", layout="wide")

st.markdown("""
<style>
.metric-card {
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 60%, #0f3460 100%);
    padding: 1.4rem 1.2rem;
    border-radius: 14px;
    color: white;
    text-align: center;
    margin: 0.4rem 0;
    box-shadow: 2px 4px 12px rgba(0,0,0,0.2);
    border: 1px solid #2a2a3f;
}
.metric-card h2 { margin: 0; font-size: 1.8rem; font-weight: 700; color: #e2b96f; }
.metric-card p  { margin: 0.3rem 0 0; font-size: 0.85rem; color: #cbd5e0; letter-spacing: 0.03em; }
.section-header {
    font-size: 1.05rem; font-weight: 600; color: #cbd5e0; margin: 1.2rem 0 0.5rem;
    border-left: 4px solid #e2b96f; padding: 0.4rem 0.6rem; background: #16213e; border-radius: 0 6px 6px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------- DATA LOADING ----------
DATA_PATH = "Bookings.csv"
if os.path.exists(DATA_PATH):
    df_raw = load_data(DATA_PATH)
    st.sidebar.success("✅ Dataset Loaded")
else:
    st.error(f"Dataset '{DATA_PATH}' not found. Please ensure the CSV is in the same folder as this script.")
    st.stop()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Filters")

vehicle_options = sorted(df_raw['Vehicle_Type'].dropna().unique())
selected_vehicles = st.sidebar.multiselect("Vehicle Type", vehicle_options, default=vehicle_options)

status_options = sorted(df_raw['Booking_Status'].dropna().unique())
selected_status = st.sidebar.multiselect("Booking Status", status_options, default=status_options)

payment_options = sorted(df_raw['Payment_Method'].dropna().unique())
selected_payments = st.sidebar.multiselect("Payment Method", payment_options, default=payment_options)

# Filtering logic
df = df_raw[
    df_raw['Vehicle_Type'].isin(selected_vehicles) &
    df_raw['Booking_Status'].isin(selected_status)
].copy()

successful = df[df['Booking_Status'] == 'Success'].copy()
successful_pay = successful[successful['Payment_Method'].isin(selected_payments)]

# ---------- TITLE ----------
st.title("Ola Ride Analytics 🚖")
st.markdown("---")

# ---------- KPI CARDS ----------
total_bookings   = len(df)
success_rate     = (len(successful) / total_bookings * 100) if total_bookings > 0 else 0
total_revenue    = successful['Booking_Value'].sum()
avg_ride_value   = successful['Booking_Value'].mean() if len(successful) > 0 else 0

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(metric_card(indian_num(total_bookings), "Total Bookings"), unsafe_allow_html=True)
with c2: st.markdown(metric_card(f"{success_rate:.1f}%", "Booking Success Rate"), unsafe_allow_html=True)
with c3: st.markdown(metric_card(inr(total_revenue), "Total Revenue"), unsafe_allow_html=True)
with c4: st.markdown(metric_card(inr(avg_ride_value), "Avg Ride Value"), unsafe_allow_html=True)

st.markdown("---")

# ---------- CHARTS ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">Booking Status Breakdown</p>', unsafe_allow_html=True)
    status_counts = df['Booking_Status'].value_counts()
    colors = ['#2ecc71' if s == 'Success' else '#e74c3c' if 'Driver' in s else '#e67e22' if 'Customer' in s else '#95a5a6'
              for s in status_counts.index]
    fig, ax = styled_fig(6, 3.5)
    bars = ax.barh(status_counts.index, status_counts.values, color=colors)
    ax.set_xlabel('Rides')
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown('<p class="section-header">Revenue by Vehicle Type</p>', unsafe_allow_html=True)
    rev_by_vehicle = successful.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values(ascending=True)
    fig, ax = styled_fig(6, 3.5)
    rev_by_vehicle.plot(kind='barh', ax=ax, color='#3498db')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1e5:.1f}L'))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

# Heatmap
st.markdown('<p class="section-header">Booking Demand Heatmap</p>', unsafe_allow_html=True)
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = df.groupby(['Day_of_Week','Hour'])['Booking_ID'].count().unstack().reindex(day_order)
fig, ax = styled_fig(14, 4)
sns.heatmap(pivot, cmap='YlOrRd', ax=ax)
st.pyplot(fig)
plt.close()

# Row 4: Peak T-test
st.markdown('<p class="section-header">Ride Distance: Peak vs Off-Peak Statistical Analysis</p>', unsafe_allow_html=True)
peak = successful[successful['Hour'].between(17, 21)]['Ride_Distance'].dropna()
off_peak = successful[~successful['Hour'].between(17, 21)]['Ride_Distance'].dropna()

if not peak.empty and not off_peak.empty:
    t_stat, p_val = ttest_ind(peak, off_peak, equal_var=False)
    col_left, col_right = st.columns([1, 2])
    with col_left:
        st.info(f"**P-Value:** {p_val:.4f}\n\n"
                f"**Conclusion:** {'Significant' if p_val < 0.05 else 'Not Significant'}")
    with col_right:
        fig, ax = styled_fig(8, 4)
        sns.boxplot(data=[off_peak, peak], ax=ax, palette=['#3498db', '#e74c3c'])
        ax.set_xticklabels(['Off-Peak', 'Peak'])
        st.pyplot(fig)
        plt.close()

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>MBA Data Portfolio | Ola Ride Analytics</p>", unsafe_allow_html=True)
