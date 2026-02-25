# 🚖 Ola Ride Analytics: End-to-End Data Portfolio

A comprehensive data engineering and analytics project simulating a real-world ride-sharing environment in Bangalore. This project covers the full pipeline: **Extraction (SQL)**, **Statistical Validation (Python)**, **Business Intelligence (Power BI)**, and **Interactive Deployment (Streamlit)**.

---

## 📊 Project Overview
The objective is to analyze ride-sharing performance metrics, identify factors affecting booking success, and perform statistical testing on ride distances during peak hours.

### Key Features:
* **SQL Intelligence**: 10 complex business queries including top-performing vehicle types and cancellation reasons.
* **Python Statistical Testing**: Conducted **T-tests** to analyze variance between peak and off-peak ride distances.
* **Interactive Dashboard**: A real-time Streamlit app featuring custom CSS and geographic mapping of Bangalore hotspots.
* **Power BI Visualization**: Multi-view dashboard focusing on Revenue, Performance, and Satisfaction.

---

## 🛠️ Technical Stack & Core Logic

### 1. Database Layer: SQL Operations 🗄️
**File:** `Ola.sql`  
* **Logic:** Transforms raw booking data into high-value business views.
* **Operations:** Handles aggregations (Total Revenue) and conditional filtering (Cancellation Distribution).

### 2. Statistical Layer: Python EDA 🐍
**File:** `Ola_Python_Analysis_.ipynb` / `streamlit.py`
* **Scientific Logic:** Performs an **Independent T-Test** using `scipy.stats`.
* **Hypothesis:** Compares average ride distances during Peak (17:00–21:00) vs. Off-Peak hours to determine if shifts in distance are statistically significant.

### 3. Application Layer: Streamlit Dashboard 🚀
**File:** `streamlit.py`
* **Geospatial Mapping**: Uses a custom coordinate lookup table for 50+ Bangalore neighborhoods to render interactive maps.
* **State Management**: Implements `@st.cache_data` to optimize CSV loading and filter responsiveness.
* **Custom UI**: Injects CSS for "Dark Mode" metric cards and professional layout.

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `Bookings.csv` | Dataset containing 100,000+ ride records. |
| `Ola.sql` | SQL scripts for business KPI extraction. |
| `Ola_Python_Analysis_.ipynb` | Jupyter Notebook for data cleaning and EDA. |
| `streamlit.py` | Python script for the interactive web-based dashboard. |
| `Ola Data Analyst.pbix` | Power BI file for visual storytelling. |
| `requirements.txt` | Environment dependencies. |

---

## ⚙️ Installation & Usage

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/ola-ride-analytics.git](https://github.com/your-username/ola-ride-analytics.git)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt

3. **Launch the Dashboard:**
   ```bash
   streamlit run streamlit.py

---

## 📈 Key Insights
* **Revenue Drivers**: Prime Sedans consistently generate the highest revenue per ride.
* **Operational Bottlenecks**: Driver cancellations are primarily driven by personal issues, while customer cancellations spike during evening peaks.
* **Statistical Significance**: T-testing validates whether ride distances significantly differ during peak traffic hours, assisting in supply-side planning.

---

## 🛠️ Roadmap & Future Enhancements (WIP) 🚧
This project is currently a **Work-In-Progress**. Future updates will include:
* **Predictive Analytics**: Integration of Machine Learning models (Random Forest/XGBoost) to predict ride cancellations, following the completion of my ML certification.
* **Dynamic Geocoding**: Real-time coordinate fetching for broader location support.
* **Automated Data Pipeline**: Transitioning from static CSV to a live SQL database connection.

---
**Developed by Daksh Sharma** | *Data Analytics & Business Intelligence Portfolio*


