# 🚖 Ola Ride Analytics — End-to-End Data Portfolio

Ola processes millions of rides daily across India, yet operational leakage — from driver cancellations, incomplete rides, and peak-hour supply-demand mismatches — directly erodes both revenue and platform trust. This project quantifies where and why rides fail, statistically validates whether peak-hour behaviour differs from off-peak, and surfaces the revenue implications of operational gaps across vehicle types.

### 🔗 Live Dashboard: [ola-data-analytics-e9jsowul8qsu99z6odvwbj.streamlit.app](https://ola-data-analytics-e9jsowul8qsu99z6odvwbj.streamlit.app/)

---

## 📊 Project Overview

The full pipeline spans four layers: **Extraction (SQL)** → **Statistical Validation (Python)** → **Business Intelligence (Power BI)** → **Interactive Deployment (Streamlit)** — built on a dataset of 100,000+ ride records from Bangalore.

### Key Features
- **SQL Intelligence:** 13 business queries including window functions, CTEs, and subqueries covering cancellation rates, revenue segmentation, and driver performance ranking.
- **Python Statistical Testing:** Independent T-Test (`scipy.stats`) comparing average ride distances during Peak (17:00–21:00) vs. Off-Peak hours, with business implications derived from the result.
- **Interactive Streamlit Dashboard:** Real-time filtering, custom CSS dark-mode metric cards, and geospatial mapping of 50+ Bangalore hotspots.
- **Power BI Report:** Multi-view dashboard covering Revenue, Operational Performance, and Customer Satisfaction.

---

## 📈 Key Insights

**1. Revenue-Risk in Prime Sedan**
Prime Sedan generates the highest revenue per ride but has the widest spread between maximum and minimum driver ratings across all vehicle types. This signals inconsistent service quality — a churn risk in the premium segment where customer switching cost is lowest and competition from Uber Black is most direct.

**2. Cancellation Timing Pattern**
Customer cancellations spike during evening peak hours (5–9 PM) — the same window where Prime Sedan demand is highest. This is not a demand problem; it is a supply-response failure. Improving driver availability and incentive structures in this window is the single highest-leverage operational fix available.

**3. Peak vs. Off-Peak Ride Distance — T-Test Finding**
Statistical testing confirms [significant / no significant] difference in average ride distances between peak and off-peak hours (p = 0.080046).
- **If significant:** Peak-hour demand skews toward longer, higher-value trips — validating dynamic surge pricing as both a revenue and supply-management tool.
- **If not significant:** Trip intent does not change during peak hours, meaning cancellations — not trip length — are the primary operational problem to solve.

**4. UPI Dominance and Margin Implication**
UPI is the dominant payment method by volume. Given India's zero-MDR policy, heavy UPI concentration compresses Ola's per-transaction payment economics. Identifying customer segments that prefer card or wallet payments could guide targeted incentives to shift the payment mix toward higher-margin instruments.

**5. Incomplete Rides as Hidden Revenue Leakage**
Incomplete rides represent lost fare revenue plus potential driver penalty exposure. Cross-referencing incomplete ride reasons with vehicle type (from SQL) reveals whether this is a driver-side behavioural issue or a route/navigation failure — determining which team owns the fix.

---

## 🛠️ Technical Stack

| Layer | Tool | Purpose |
| :--- | :--- | :--- |
| Database | MySQL | Business KPI extraction, cancellation analysis |
| Statistics | Python / scipy | Hypothesis testing on peak vs. off-peak behaviour |
| Visualisation | Power BI | Revenue, performance, and satisfaction dashboards |
| Application | Streamlit | Live interactive deployment with geospatial mapping |

---

## 🗄️ SQL Highlights

Beyond standard aggregations, the SQL layer includes:

**Window Function — Driver ranking by rating within vehicle type:**
```sql
SELECT Vehicle_Type, Driver_ID, Driver_Ratings,
  RANK() OVER (PARTITION BY Vehicle_Type ORDER BY Driver_Ratings DESC) AS Rating_Rank
FROM Bookings
WHERE Booking_Status = 'Success';
```

**Subquery — High-value customers above platform average:**
```sql
SELECT Customer_ID, AVG(Booking_Value) AS Avg_Spend
FROM Bookings
GROUP BY Customer_ID
HAVING AVG(Booking_Value) > (SELECT AVG(Booking_Value) FROM Bookings)
ORDER BY Avg_Spend DESC;
```

**CTE — Cancellation rate by vehicle type:**
```sql
WITH TotalRides AS (
  SELECT Vehicle_Type, COUNT(*) AS Total FROM Bookings GROUP BY Vehicle_Type
),
CancelledRides AS (
  SELECT Vehicle_Type, COUNT(*) AS Cancelled FROM Bookings
  WHERE Booking_Status LIKE '%Cancel%' GROUP BY Vehicle_Type
)
SELECT t.Vehicle_Type, t.Total, c.Cancelled,
  ROUND(c.Cancelled * 100.0 / t.Total, 2) AS Cancellation_Rate_Pct
FROM TotalRides t JOIN CancelledRides c ON t.Vehicle_Type = c.Vehicle_Type
ORDER BY Cancellation_Rate_Pct DESC;
```

---

## 📂 Repository Structure

| File | Description |
| :--- | :--- |
| `Bookings.csv` | 100,000+ ride records from Bangalore |
| `Ola.sql` | SQL scripts for business KPI extraction |
| `Ola_Python_Analysis_.ipynb` | Jupyter Notebook — EDA and statistical testing |
| `streamlit.py` | Interactive Streamlit dashboard |
| `Ola Data Analyst.pbix` | Power BI multi-view report |
| `requirements.txt` | Python dependencies |

---

## ⚙️ Installation & Usage

**1. Clone the repository:**
```bash
git clone https://github.com/your-username/ola-ride-analytics.git
cd ola-ride-analytics
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Launch the dashboard:**
```bash
streamlit run streamlit.py
```

---

## 🛠️ Roadmap

- **Near-term:** Logistic regression model (`sklearn`) to predict ride cancellation probability based on time-of-day, vehicle type, and pickup zone — no additional certification required.
- **Post-certification:** XGBoost cancellation model with SHAP explainability for feature interpretation; transition from static CSV to live MySQL connection.
- **Long-term:** Real-time data pipeline for live operational monitoring.

---

**Developed by Daksh Sharma** | *Data Analytics & Business Intelligence Portfolio*

