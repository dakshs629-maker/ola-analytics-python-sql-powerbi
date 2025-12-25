Ola Ride Analytics Dashboard (Power BI & SQL)

End‑to‑end data analytics project simulating a ride‑hailing company in Bengaluru, using a synthetic dataset of 100k+ rides for one month to analyze demand, revenue, cancellations, and service quality, similar to what an entry-level data analyst would do in a mobility company.

​Note: Data is fully synthetic and generated via LLM prompts for learning; this project is not affiliated with Ola or ANI Technologies Pvt. Ltd.

-Business questions

# How many rides succeed vs. fail, and how do success and cancellation rates vary by day, weekend, and vehicle type?
​# Which vehicle types and customers contribute the most distance and revenue?
​# What are the main reasons for customer and driver cancellations and incomplete rides?
​# How do driver and customer ratings differ across vehicle types, and how are they correlated?
​
-Data

Each record represents one ride with: date/time, booking and customer IDs, booking status, vehicle type, pickup/drop locations, VTAT, CTAT, cancellation and incomplete‑ride reasons, booking value, payment method, ride distance, and both driver and customer ratings.
#​Constraints built into the data:
   ~62% successful bookings; customer cancellations <7%, driver cancellations <18%, incomplete rides <6%.
​   ~Higher order volume and booking value on weekends and match days.
​
-SQL work

#Created an Ola database and a bookings table to store all rides.
​#Built reusable SQL views to answer core questions, such as:
       >Successful_Bookings – all successful rides.
       ​>ride_distance_for_each_vehicle – average distance by vehicle type.
       ​>Top_5_Customers – most active customers by number of rides.
       ​>total_successful_ride_value – total revenue from successful rides.
​
-Power BI dashboard

#Multi‑page dashboard with:
      >Overview – ride volume over time and booking status breakdown.
​      >Vehicle & revenue – top vehicle types by distance, revenue by payment method, top customers by booking value, ride distance distribution per day.
​      >Cancellations – reasons for customer and driver cancellations.
​      >Ratings – distributions of driver and customer ratings and a customer‑vs‑driver rating comparison.

-Python exploration
#The ola_python_analysis.ipynb notebook contains additional EDA using pandas, seaborn, and matplotlib, including booking‑value distributions, cancellation breakdowns for Prime Sedan rides, and relationships between booking value and VTAT.
​
​-Tech stack

#SQL: data querying and creation of analytical views.
​#Power BI: data modelling and interactive dashboards.

-How to run

#Clone the repo and open Bookings.csv in your SQL/BI environment.
​#Run Ola.sql to create the database, table, and analysis views.
​#Open Ola Data Analyst.pbix in Power BI and refresh the data source.
​#Open ola_python_analysis.ipynb to explore the pandas/seaborn analysis.
​

