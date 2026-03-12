 Airline Ticket Prices — Data Analytics 

An end-to-end data analytics project using **Python**, **SQLite (SQL)**, **Pandas**, and **Matplotlib** to explore 250 international airline ticket records.

---

##  Questions & Key Findings

| # | Question | Finding |
|---|----------|---------|
| Q1 | Which airline has the highest avg price? | **Saudia** leads at $2,389 avg |
| Q2 | How does ticket class affect price? | **First** is 2.9× more expensive than Economy |
| Q3 | Does booking earlier save money? | Booking lead time has **minimal effect** on price |
| Q4 | What are the most expensive routes? | **London→Dubai** tops the chart at ~$3,846 |
| Q5 | Which class gives best value per km? | **Economy** at $0.18/km vs First at $0.56/km |

---


## 🛠️ Tech Stack

- **Python 3.9+**
- **SQLite** — in-memory database for SQL queries
- **Pandas** — data loading & manipulation
- **Matplotlib** — data visualisation
- **NumPy** — numerical operations (trend lines)

---

## 📝 SQL Queries

### Average price by airline
```sql
SELECT Airline,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       COUNT(*)                 AS Tickets
FROM   tickets
GROUP  BY Airline
ORDER  BY Avg_Price DESC;
```

### Price stats by class
```sql
SELECT Class,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       ROUND(MIN(Price_USD), 2) AS Min_Price,
       ROUND(MAX(Price_USD), 2) AS Max_Price
FROM   tickets
GROUP  BY Class
ORDER  BY Avg_Price DESC;
```

### Booking timing vs price
```sql
SELECT Days_Before_Departure,
       ROUND(AVG(Price_USD), 2) AS Avg_Price,
       Class
FROM   tickets
GROUP  BY Days_Before_Departure, Class
ORDER  BY Days_Before_Departure;
```

### Top 10 most expensive routes
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

###  Value per kilometre by class
```sql
SELECT Class,
       ROUND(AVG(Price_USD / Distance_km), 4) AS Price_Per_Km,
       ROUND(AVG(Price_USD), 2)               AS Avg_Price,
       ROUND(AVG(Distance_km), 0)             AS Avg_Distance
FROM   tickets
GROUP  BY Class
ORDER  BY Price_Per_Km;
```


