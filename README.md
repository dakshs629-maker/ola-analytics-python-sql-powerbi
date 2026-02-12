📌 Project Overview
This project analyzes a dataset of 100,000 Ola rides to uncover patterns in customer behavior, driver performance, and revenue distribution. By combining SQL for data transformation and Power BI for visualization, the project provides a comprehensive look at urban mobility trends.


🛠️ Tech Stack
-SQL: Data extraction, cleaning, and creating business-logic Views.

-Power BI: Data modeling, DAX calculations, and interactive visualization.

-Excel: Initial data exploration and formatting.


💾 SQL Analysis & Data Transformation

To prepare the data for the dashboard, I created specific SQL Views to answer key business questions.

Key Queries Implemented:
   *Successful Bookings: Filtering all completed rides for revenue analysis.

   *Ride Distance by Vehicle: Calculating average distances for different categories (Prime Sedan, Mini, Bike, etc.).

   *Cancellation Tracking: Identifying the top reasons for cancellations by both customers and drivers.

   *Rating Analysis: Aggregating driver and customer ratings to monitor service quality.

SQL
-- Example: Creating a view for successful bookings
CREATE VIEW Successful_Bookings AS
SELECT * FROM bookings
WHERE Booking_Status = 'Success';

-- Example: Finding the top 5 customers by total booking value
CREATE VIEW Top_5_Customers AS
SELECT TOP 5 Customer_ID, SUM(Booking_Value) as Total_Value
FROM bookings
GROUP BY Customer_ID
ORDER BY Total_Value DESC;


📊 Dashboard Features & KPIs
The Power BI dashboard consists of five specialized views to provide deep-dive insights:

1. Overall: High-level KPIs including Booking Value, Ride Volume, and Total Distance.

2. Vehicle Type: Analysis of performance across different segments (Auto, Prime, Mini).

3. Revenue: Tracking revenue concentration across cities and time periods.

4. Cancellations: Visualizing the "why" behind cancelled rides to improve retention.

5. Ratings: A scorecard for driver and customer satisfaction.


💡 Key Insights

*Revenue Concentration: City A and City B are the primary drivers of growth, contributing over 60% of total revenue.

*Peak Demand: Demand spikes significantly during evening time slots across all urban centers.

*Operational Hurdles: Cancellation rates are highest during peak hours, often due to "Driver not moving towards pickup" or "Personal reasons".


📂 Project Structure

Ola Data Analyst.pbix: The complete Power BI project file.

Ola.sql: The SQL script containing all 10 business logic views.

data/: Raw dataset (synthetic).
