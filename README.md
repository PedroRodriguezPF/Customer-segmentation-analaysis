# Customer Segmentation Analysis (RFM) Project

## Overview
This project performs customer segmentation using RFM analysis (Recency, Frequency, Monetary) on a retail dataset.  
The objective is to identify different types of customers and generate business insights and marketing strategies based on their purchasing behavior.

This project covers the full data analysis process:
- Data exploration
- Data cleaning
- Feature engineering
- RFM calculation
- Customer segmentation
- Business insights
- Data visualization
- Exporting results

The analysis was implemented in Python using pandas, numpy, matplotlib, and datetime.

---

## Dataset
The dataset used is the Online Retail Dataset, which contains transactions from an online store.

Main columns used:
- InvoiceNo
- StockCode
- Description
- Quantity
- InvoiceDate
- UnitPrice
- CustomerID
- Country

---

## Project Structure
```
Customer_analysis_project/
│
├── online_retail.csv
├── analisis.py
├── rfm_analysis_results.csv
├── segment_summary.csv
├── segment_recommendations.csv
└── README.md
```

---

## Data Cleaning
The following cleaning steps were performed:
- Removed rows with missing CustomerID
- Removed returns (Quantity < 0)
- Removed transactions with UnitPrice ≤ 0
- Created a new column: Revenue = Quantity × UnitPrice
- Converted InvoiceDate to datetime format
- Converted CustomerID to string

---

## RFM Analysis
RFM analysis is a customer segmentation technique based on:

| Metric | Description |
|-------|-------------|
| Recency | Days since last purchase |
| Frequency | Number of purchases |
| Monetary | Total money spent |

Steps performed:
1. Group data by CustomerID
2. Calculate Recency, Frequency, Monetary
3. Create RFM scores using quartiles
4. Calculate combined RFM Score
5. Segment customers

---

## Customer Segments
Customers were classified into the following segments:

| Segment | Description |
|--------|-------------|
| Champions | Best customers |
| Loyal | Frequent customers |
| At Risk | Customers who haven't purchased recently |
| Others | Average customers |

---

## Business Insights
The script automatically identifies:
- Segment generating the most revenue
- Segment with most customers
- Segment with highest frequency
- Segment at highest risk of churn

It also generates marketing strategies for each segment:
- Champions → Loyalty programs & rewards
- Loyal → Cross-selling & promotions
- At Risk → Reactivation campaigns
- Others → General marketing campaigns

---

## Visualizations
The project includes visualizations for:
- Distribution of customer spending
- Number of customers per segment
- Revenue per segment
- Average frequency per segment
- Average recency per segment

---

## Outputs
The project exports the following files:
- `rfm_analysis_results.csv` → Full RFM table per customer
- `segment_summary.csv` → Summary per segment
- `segment_recommendations.csv` → Marketing strategies per segment

---

## How to Run the Project

1. Install dependencies:
```
pip install pandas matplotlib numpy
```

2. Make sure the dataset is in the same folder as the script:
```
online_retail.csv
```

3. Run the script:
```
python analisis.py
```

---

## Skills Demonstrated
This project demonstrates the following data analysis skills:
- Data cleaning
- Exploratory Data Analysis (EDA)
- Feature engineering
- Customer segmentation
- Business analysis
- Data visualization
- Python (pandas, numpy, matplotlib)

---

## Business Value of the Project
This type of analysis helps companies:
- Identify their most valuable customers
- Reduce customer churn
- Improve marketing strategies
- Increase customer lifetime value
- Personalize promotions

---

## Author
Pedro Rodriguez  
Aspiring Data Analyst | Python | SQL | Data Visualization | Business Analysis
