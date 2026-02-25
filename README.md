# Ola Ride Analytics — End-to-End Data Analysis Project

A full-stack data analysis project on Ola ride bookings covering SQL querying, Python EDA, Power BI dashboarding, and an interactive Streamlit web app.

---

## Project Overview

This project analyses a synthetic Ola bookings dataset of **103,024 rides** from July 2024 across Bangalore. The goal is to uncover operational inefficiencies, revenue patterns, and customer behaviour using multiple analytical tools.

---

## Dataset

| Field | Detail |
|---|---|
| Source | Synthetic / practice dataset |
| Period | July 2024 |
| Records | 103,024 rows, 20 columns |
| City | Bangalore |

**Key columns:** `Booking_ID`, `Booking_Status`, `Customer_ID`, `Vehicle_Type`, `Pickup_Location`, `Drop_Location`, `Booking_Value`, `Payment_Method`, `Ride_Distance`, `Driver_Ratings`, `Customer_Rating`, `Canceled_Rides_by_Customer`, `Canceled_Rides_by_Driver`

---

## Tools & Stack

| Tool | Purpose |
|---|---|
| **SQL (MySQL)** | Data extraction, view creation, aggregations |
| **Python (Pandas, Seaborn, Matplotlib, SciPy)** | EDA, statistical testing, segmentation |
| **Power BI** | Interactive business dashboard |
| **Streamlit** | Web app deployment |

---

## Project Structure

```
ola-ride-analytics/
│
├── Bookings.csv                        # Raw dataset
├── Ola.sql                             # SQL queries & views
├── Ola_Python_Analysis_Improved.ipynb  # Python EDA notebook
├── Ola_Data_Analyst.pbix               # Power BI dashboard
├── app.py                              # Streamlit web app
└── README.md
```

---

## Key Findings

1. **62% booking success rate** — 18% of rides are cancelled by drivers, the single largest source of failed bookings
2. **Evening hours (17–21) drive peak demand** — surge pricing opportunity exists in these slots
3. **Prime SUV and Prime Sedan** command the highest average booking value — premium fleet expansion could increase revenue
4. **Cash dominates at 54%** with UPI at 40% — room to accelerate digital payment adoption
5. **Driver ratings are uniformly high (>4.0)** across all vehicle types — rating system may need review
6. **Ride distance is the strongest predictor of booking value** — distance-based dynamic pricing is viable
7. **VIP customers (spend >₹3,000)** represent a small but high-value segment — loyalty programme opportunity

---

## Statistical Analysis

- **One-Way ANOVA** — Booking value differs significantly across vehicle types (p < 0.05)
- **Welch's t-test** — Ride distance during peak hours (17–21) vs off-peak tested for significance
- **Chi-Square Test** — Association between payment method and vehicle type

---

## Machine Learning *(In Progress)*

ML extensions planned after completing the **Google Advanced Data Analytics Certificate**:

| Model | Target | Goal |
|---|---|---|
| Logistic Regression | Booking success (binary) | Predict whether a ride will complete |
| Random Forest / XGBoost | Cancellation risk | Identify high-risk bookings before they cancel |
| Linear Regression | Booking value | Predict fare from distance, vehicle type, time |
| K-Means Clustering | Customer segments | Data-driven RFM segmentation |

> Models will be added to the existing notebook once training is complete.

---

## Python Notebook Sections

- Data Quality Check
- Key Performance Indicators (KPIs)
- Booking Status Distribution
- Cancellation Deep Dive
- Vehicle Type Performance
- Payment Method Analysis
- Time-Based Trends
- Customer Segmentation (RFM-lite)
- Ratings Analysis
- Incomplete Rides Analysis
- Statistical Analysis
- Vehicle Type Scorecard
- Key Insights Summary

---

## SQL Queries Covered

- Successful bookings view
- Average ride distance by vehicle type
- Top 5 customers by ride count
- Driver cancellations by reason
- Max/min driver ratings for Prime Sedan
- UPI payment rides
- Total revenue from successful rides
- Incomplete rides with reasons

---

## Streamlit App

The web app provides an interactive dashboard with:
- KPI metric cards (total bookings, revenue, success rate, avg ride value)
- Sidebar filters by vehicle type, booking status, and payment method
- Booking status breakdown
- Revenue and ride volume by vehicle type
- Hourly demand heatmap
- Payment method distribution
- Customer segmentation chart
- Peak vs off-peak ride distance comparison

**Run locally:**
```bash
pip install streamlit pandas matplotlib seaborn scipy
streamlit run app.py
```

---

## Author

MBA Data Portfolio — Delhi, India
