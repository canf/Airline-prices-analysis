# ✈️ Airline Ticket Prices — Data Analytics Portfolio

An end-to-end data analytics project using **Python**, **SQLite (SQL)**, **Pandas**, and **Matplotlib** to explore 250 international airline ticket records.

---

## 📁 Project Structure

```
airline_project/
├── analysis.py                        # Main analysis script
├── airline_ticket_prices_dataset.csv  # Dataset (250 records)
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
└── output/                            # Auto-generated charts
    ├── q1_avg_price_by_airline.png
    ├── q2_price_by_class.png
    ├── q3_booking_timing.png
    ├── q4_top_routes.png
    └── q5_value_per_km.png
```

---

## 📊 Dataset

| Column                  | Type    | Description                         |
|-------------------------|---------|-------------------------------------|
| `Ticket_ID`             | int     | Unique ticket identifier            |
| `Airline`               | string  | Carrier name (8 airlines)           |
| `Origin`                | string  | Departure city                      |
| `Destination`           | string  | Arrival city                        |
| `Distance_km`           | int     | Route distance in kilometres        |
| `Class`                 | string  | Economy / Business / First          |
| `Days_Before_Departure` | int     | Booking lead time (days)            |
| `Price_USD`             | float   | Ticket price in US dollars          |

---

## ❓ Questions & Key Findings

| # | Question | Finding |
|---|----------|---------|
| Q1 | Which airline has the highest avg price? | **Saudia** leads at $2,389 avg |
| Q2 | How does ticket class affect price? | **First** is 2.9× more expensive than Economy |
| Q3 | Does booking earlier save money? | Booking lead time has **minimal effect** on price |
| Q4 | What are the most expensive routes? | **London→Dubai** tops the chart at ~$3,846 |
| Q5 | Which class gives best value per km? | **Economy** at $0.18/km vs First at $0.56/km |

---

## 🚀 How to Run

### 1. Clone / download the project
```bash
git clone https://github.com/your-username/airline-analytics.git
cd airline-analytics
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the analysis
```bash
python analysis.py
```

Charts are saved to the `output/` folder automatically.

---

## 🛠️ Tech Stack

- **Python 3.9+**
- **SQLite** — in-memory database for SQL queries
- **Pandas** — data loading & manipulation
- **Matplotlib** — data visualisation
- **NumPy** — numerical operations (trend lines)

---

## 📝 SQL Queries

### Q1 — Average price by airline
```sql
SELECT Airline,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       COUNT(*)                 AS Tickets
FROM   tickets
GROUP  BY Airline
ORDER  BY Avg_Price DESC;
```

### Q2 — Price stats by class
```sql
SELECT Class,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       ROUND(MIN(Price_USD), 2) AS Min_Price,
       ROUND(MAX(Price_USD), 2) AS Max_Price
FROM   tickets
GROUP  BY Class
ORDER  BY Avg_Price DESC;
```

### Q3 — Booking timing vs price
```sql
SELECT Days_Before_Departure,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       Class
FROM   tickets
GROUP  BY Days_Before_Departure, Class
ORDER  BY Days_Before_Departure;
```

### Q4 — Top 10 most expensive routes
```sql
SELECT Origin || ' → ' || Destination AS Route,
       ROUND(AVG(Price_USD), 2)        AS Avg_Price,
       COUNT(*)                         AS Tickets
FROM   tickets
GROUP  BY Origin, Destination
HAVING Tickets >= 3
ORDER  BY Avg_Price DESC
LIMIT  10;
```

### Q5 — Value per kilometre by class
```sql
SELECT Class,
       ROUND(AVG(Price_USD / Distance_km), 4) AS Price_Per_Km,
       ROUND(AVG(Price_USD), 2)               AS Avg_Price,
       ROUND(AVG(Distance_km), 0)             AS Avg_Distance
FROM   tickets
GROUP  BY Class
ORDER  BY Price_Per_Km;
```

---

## 📄 License
MIT — free to use and modify for your own portfolio.
