import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import seaborn as sns

# Global dark chart theme
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
from scipy.stats import ttest_ind
import os

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Ola Ride Analytics",
    page_icon="🚖",
    layout="wide"
)

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
}
.metric-card h2 { margin: 0; font-size: 1.8rem; font-weight: 700; color: #e2b96f; }
.metric-card p  { margin: 0.3rem 0 0; font-size: 0.85rem; color: #cbd5e0; letter-spacing: 0.03em; }
.section-header {
    font-size: 1.05rem;
    font-weight: 600;
    color: #cbd5e0;
    margin: 1.2rem 0 0.5rem;
    border-left: 4px solid #e2b96f;
    padding: 0.4rem 0.6rem;
    background: #16213e;
    border-radius: 0 6px 6px 0;
}
</style>
""", unsafe_allow_html=True)


# ---------- HELPERS ----------
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
        return str(num)

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

def metric_card(value, label):
    return f'<div class="metric-card"><h2>{value}</h2><p>{label}</p></div>'

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df.drop(columns=['Vehicle Images', 'Unnamed: 20'], inplace=True, errors='ignore')
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Hour'] = df['Date'].dt.hour
    df['Day_of_Week'] = df['Date'].dt.day_name()
    df['Booking_Value'] = pd.to_numeric(df['Booking_Value'], errors='coerce')
    df['Ride_Distance'] = pd.to_numeric(df['Ride_Distance'], errors='coerce')
    return df


# ---------- LOAD DATA ----------
DATA_PATH = "Bookings.csv"

if os.path.exists(DATA_PATH):
    df_raw = load_data(DATA_PATH)
    st.sidebar.info("Using bundled dataset")
else:
    st.error("Dataset not found. Please ensure the CSV is in the repository.")
    st.stop()


# ---------- SIDEBAR FILTERS ----------
st.sidebar.header("Data")
st.sidebar.file_uploader("Upload Bookings CSV", type="csv", disabled=True)
st.sidebar.markdown("---")
st.sidebar.header("Filters")

vehicle_options = sorted(df_raw['Vehicle_Type'].dropna().unique())
selected_vehicles = st.sidebar.multiselect("Vehicle Type", vehicle_options, default=vehicle_options)

status_options = sorted(df_raw['Booking_Status'].dropna().unique())
selected_status = st.sidebar.multiselect("Booking Status", status_options, default=status_options)

payment_options = sorted(df_raw['Payment_Method'].dropna().unique())
selected_payments = st.sidebar.multiselect("Payment Method", payment_options, default=payment_options)

df = df_raw[
    df_raw['Vehicle_Type'].isin(selected_vehicles) &
    df_raw['Booking_Status'].isin(selected_status)
].copy()

successful = df[df['Booking_Status'] == 'Success'].copy()
successful_pay = successful[successful['Payment_Method'].isin(selected_payments)]


# ---------- TITLE ----------
st.title("Ola Ride Analytics")
st.markdown("Interactive Analytics Dashboard")
st.markdown("---")


# ---------- KPI CARDS ----------
total_bookings   = len(df)
success_rate     = len(successful) / total_bookings * 100 if total_bookings else 0
total_revenue    = successful['Booking_Value'].sum()
avg_ride_value   = successful['Booking_Value'].mean()

c1, c2, c3, c4 = st.columns(4)
c1.markdown(metric_card(indian_num(total_bookings), "Total Bookings"), unsafe_allow_html=True)
c2.markdown(metric_card(f"{success_rate:.1f}%", "Booking Success Rate"), unsafe_allow_html=True)
c3.markdown(metric_card(inr(total_revenue), "Total Revenue"), unsafe_allow_html=True)
c4.markdown(metric_card(inr(avg_ride_value), "Avg Ride Value"), unsafe_allow_html=True)

st.markdown("---")


# ---------- ROW 1: Booking Status + Vehicle Revenue ----------
col1, col2 = st.columns(2)

with col1:
    st.markdown('<p class="section-header">Booking Status Breakdown</p>', unsafe_allow_html=True)
    status_counts = df['Booking_Status'].value_counts()
    colors = ['#2ecc71' if s == 'Success' else '#e74c3c' if 'Driver' in s else '#e67e22' if 'Customer' in s else '#95a5a6'
              for s in status_counts.index]
    fig, ax = styled_fig(6, 3.5)
    bars = ax.barh(status_counts.index, status_counts.values, color=colors, edgecolor='none')
    for bar, val in zip(bars, status_counts.values):
        ax.text(val + 200, bar.get_y() + bar.get_height()/2, f'{val:,}', va='center', fontsize=9)
    ax.set_xlabel('Rides', fontsize=9)
    ax.tick_params(labelsize=9)
    ax.spines[['top','right','left']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col2:
    st.markdown('<p class="section-header">Revenue by Vehicle Type</p>', unsafe_allow_html=True)
    rev_by_vehicle = successful.groupby('Vehicle_Type')['Booking_Value'].sum().sort_values(ascending=True)
    fig, ax = styled_fig(6, 3.5)
    bars = ax.barh(rev_by_vehicle.index, rev_by_vehicle.values,
                   color=sns.color_palette('Blues_d', len(rev_by_vehicle)), edgecolor='none')
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(lambda x, _: f'₹{x/1e6:.1f}M'))
    ax.tick_params(labelsize=9)
    ax.spines[['top','right','left']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ---------- ROW 2: Hourly Heatmap ----------
st.markdown('<p class="section-header">Booking Demand: Hour of Day × Day of Week</p>', unsafe_allow_html=True)
day_order = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
pivot = df.groupby(['Day_of_Week','Hour'])['Booking_ID'].count().unstack().reindex(day_order)
fig, ax = styled_fig(14, 3.5)
sns.heatmap(pivot, cmap='YlOrRd', linewidths=0.2, annot=False, ax=ax, cbar_kws={'shrink': 0.6})
ax.set_xlabel('Hour of Day', fontsize=9)
ax.set_ylabel('')
ax.tick_params(labelsize=8)
plt.tight_layout()
st.pyplot(fig)
plt.close()


# ---------- ROW 3: Payment Method + Customer Segmentation ----------
col3, col4 = st.columns(2)

with col3:
    st.markdown('<p class="section-header">Payment Method Distribution</p>', unsafe_allow_html=True)
    pay_counts = successful_pay['Payment_Method'].value_counts()
    fig, ax = styled_fig(6, 3.5)
    bars = ax.bar(pay_counts.index, pay_counts.values,
                  color=sns.color_palette('Set2', len(pay_counts)), edgecolor='none')
    for bar, val in zip(bars, pay_counts.values):
        ax.text(bar.get_x() + bar.get_width()/2, val + 100, f'{val:,}', ha='center', fontsize=9)
    ax.set_ylabel('Rides', fontsize=9)
    ax.tick_params(labelsize=9)
    ax.spines[['top','right','left']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

with col4:
    st.markdown('<p class="section-header">Customer Segmentation by Total Spend</p>', unsafe_allow_html=True)
    customer = successful.groupby('Customer_ID').agg(Total_Spend=('Booking_Value','sum')).reset_index()
    def segment(s):
        if s > 3000: return 'VIP (>₹3k)'
        elif s > 1000: return 'Regular (₹1k–3k)'
        else: return 'Occasional (<₹1k)'
    customer['Segment'] = customer['Total_Spend'].apply(segment)
    seg_counts = customer['Segment'].value_counts()
    colors_seg = {'VIP (>₹3k)': '#e2b96f', 'Regular (₹1k–3k)': '#0f3460', 'Occasional (<₹1k)': '#95a5a6'}
    fig, ax = styled_fig(6, 3.5)
    ax.bar(seg_counts.index, seg_counts.values,
           color=[colors_seg.get(s, '#ccc') for s in seg_counts.index], edgecolor='none')
    for i, (idx, val) in enumerate(seg_counts.items()):
        ax.text(i, val + 20, f'{val:,}', ha='center', fontsize=9)
    ax.set_ylabel('Customers', fontsize=9)
    ax.tick_params(labelsize=9)
    ax.spines[['top','right','left']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()


# ---------- ROW 4: Peak vs Off-Peak t-test ----------
st.markdown('<p class="section-header">Ride Distance: Peak (17–21) vs Off-Peak — Welch\'s t-Test</p>', unsafe_allow_html=True)

peak     = successful[successful['Hour'].between(17, 21)]['Ride_Distance'].dropna()
off_peak = successful[~successful['Hour'].between(17, 21)]['Ride_Distance'].dropna()
t_stat, p_val = ttest_ind(peak, off_peak, equal_var=False)

col5, col6 = st.columns([1, 1.6])

with col5:
    st.markdown(f"""
    <div style='background:#1a1a2e; padding:1.2rem; border-radius:10px; font-size:0.9rem; line-height:2; border: 1px solid #e2b96f; color:#e2b96f;'>
    <b>Peak mean</b>: {peak.mean():.2f} km &nbsp; (n={len(peak):,})<br>
    <b>Off-peak mean</b>: {off_peak.mean():.2f} km &nbsp; (n={len(off_peak):,})<br>
    <b>T-statistic</b>: {t_stat:.4f}<br>
    <b>P-value</b>: {p_val:.6f}<br>
    <b>Conclusion</b>: {"✅ Significant difference (p < 0.05)" if p_val < 0.05 else "❌ No significant difference (p ≥ 0.05)"}
    </div>
    """, unsafe_allow_html=True)

with col6:
    plot_df = successful.copy()
    plot_df['Period'] = plot_df['Hour'].apply(lambda h: 'Peak (17–21)' if 17 <= h <= 21 else 'Off-Peak')
    fig, ax = styled_fig(6, 4)
    sns.boxplot(x='Period', y='Ride_Distance', data=plot_df, ax=ax,
                order=['Off-Peak', 'Peak (17–21)'],
                palette=['#3498db', '#e74c3c'],
                width=0.5, flierprops=dict(marker='o', markersize=3, alpha=0.4))
    ax.set_ylabel('Ride Distance (km)', fontsize=10)
    ax.set_xlabel('Period', fontsize=10)
    ax.tick_params(labelsize=9)
    ax.set_xticklabels(['Off-Peak', 'Peak (17–21)'], fontsize=9)
    ax.annotate(f'p = {p_val:.4f}', xy=(0.5, 0.98), xycoords='axes fraction',
                ha='center', fontsize=10, weight='bold',
                color='green' if p_val < 0.05 else 'red')
    ax.spines[['top','right']].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close()


# ---------- ROW 5: Vehicle Scorecard ----------
st.markdown('<p class="section-header">Vehicle Type Performance Scorecard</p>', unsafe_allow_html=True)

scorecard = successful.groupby('Vehicle_Type').agg(
    Total_Revenue=('Booking_Value', 'sum'),
    Avg_Value=('Booking_Value', 'mean'),
    Avg_Distance=('Ride_Distance', 'mean'),
    Avg_Driver_Rating=('Driver_Ratings', 'mean'),
    Ride_Count=('Booking_ID', 'count')
).round(2).reset_index()
scorecard['Total_Revenue_Display'] = scorecard['Total_Revenue'].apply(inr)

st.dataframe(
    scorecard[['Vehicle_Type','Ride_Count','Total_Revenue_Display','Avg_Value','Avg_Distance','Avg_Driver_Rating']]
    .rename(columns={
        'Vehicle_Type': 'Vehicle',
        'Ride_Count': 'Rides',
        'Total_Revenue_Display': 'Total Revenue',
        'Avg_Value': 'Avg Value (₹)',
        'Avg_Distance': 'Avg Distance (km)',
        'Avg_Driver_Rating': 'Avg Driver Rating'
    }),
    use_container_width=True,
    hide_index=True
)


# ---------- ROW 6: Pickup and Dropoff Map ----------
st.markdown('<p class="section-header">Pickup & Dropoff Locations Map</p>', unsafe_allow_html=True)

@st.cache_data
def geocode_locations(locations):
    """Geocode location names to coordinates using geopy with error handling"""
    from geopy.geocoders import Nominatim
    from geopy.exc import GeocoderTimedOut
    import time
    
    geocoder = Nominatim(user_agent="ola_analytics", timeout=10)
    coords = {}
    
    for i, loc in enumerate(locations):
        try:
            # Try with Bangalore context first
            location = geocoder.geocode(f"{loc}, Bangalore, India")
            if location:
                coords[loc] = (location.latitude, location.longitude)
            else:
                # If not found, try without context
                location = geocoder.geocode(loc)
                if location:
                    coords[loc] = (location.latitude, location.longitude)
            
            # Add delay to respect rate limits
            time.sleep(0.5)
        except GeocoderTimedOut:
            st.warning(f"⚠️ Timeout geocoding '{loc}'. Skipping...")
        except Exception as e:
            pass
    
    return coords

# Get unique locations
pickup_locs = set(successful['Pickup_Location'].dropna().unique())
dropoff_locs = set(successful['Drop_Location'].dropna().unique())
all_locations = list(pickup_locs | dropoff_locs)

st.info(f"Found {len(pickup_locs)} unique pickup locations and {len(dropoff_locs)} unique dropoff locations")

# Geocode locations
location_coords = geocode_locations(all_locations)

if location_coords:
    st.success(f"✅ Successfully geocoded {len(location_coords)}/{len(all_locations)} locations")
    
    # Map filter options
    map_filter = st.radio("Show:", ["Both", "Pickup Only", "Dropoff Only"], horizontal=True)
    
    # Prepare map data based on filter
    map_data = []
    
    # Prepare pickup locations
    if map_filter in ["Both", "Pickup Only"]:
        pickup_agg = successful['Pickup_Location'].value_counts()
        for loc, count in pickup_agg.items():
            if loc in location_coords:
                lat, lng = location_coords[loc]
                map_data.append({'latitude': lat, 'longitude': lng, 'type': 'Pickup', 'count': count, 'location': loc})
    
    # Prepare dropoff locations (always add, don't filter by whether pickup exists)
    if map_filter in ["Both", "Dropoff Only"]:
        dropoff_agg = successful['Drop_Location'].value_counts()
        for loc, count in dropoff_agg.items():
            if loc in location_coords:
                lat, lng = location_coords[loc]
                map_data.append({'latitude': lat, 'longitude': lng, 'type': 'Dropoff', 'count': count, 'location': loc})
    
    if map_data:
        map_df = pd.DataFrame(map_data)
        
        # Create custom map using folium
        import folium
        from streamlit_folium import st_folium
        
        # Calculate center of map
        center_lat = map_df['latitude'].mean()
        center_lng = map_df['longitude'].mean()
        
        m = folium.Map(location=[center_lat, center_lng], zoom_start=11, tiles="OpenStreetMap")
        
        # Add markers with different colors
        for idx, row in map_df.iterrows():
            color = '#FF6B35' if row['type'] == 'Pickup' else '#004E89'  # Orange for pickup, Blue for dropoff
            
            folium.CircleMarker(
                location=[row['latitude'], row['longitude']],
                radius=10,
                popup=f"<b>{row['location']}</b><br>{row['type']}<br>Rides: {row['count']}",
                tooltip=f"{row['location']} ({row['type']})",
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8,
                weight=2
            ).add_to(m)
        
        st_folium(m, width=1400, height=500)
        
        pickup_count = len([x for x in map_data if x['type'] == 'Pickup'])
        dropoff_count = len([x for x in map_data if x['type'] == 'Dropoff'])
        st.info(f"Showing {pickup_count} pickup locations (🟠) & {dropoff_count} dropoff locations (🔵)")
    else:
        st.warning("No location data available for selected filter")
else:
    st.warning("⚠️ Could not geocode locations. Check your internet connection and try refreshing.")


# ---------- FOOTER ----------
st.markdown("---")
st.markdown("<p style='text-align:center; color:gray; font-size:0.8rem;'>MBA Data Portfolio</p>", unsafe_allow_html=True)
