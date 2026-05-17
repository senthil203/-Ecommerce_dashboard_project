# E-Commerce Sales Analytics Dashboard

A complete end-to-end data analytics project built for a **Requirements Analyst** role.
This project analyzes 2,000 e-commerce sales transactions across India to uncover revenue trends,
customer behavior, and product performance — using Python, SQL, Excel, and Power BI.

---

## Project Overview

| Attribute        | Details                                         |
|------------------|-------------------------------------------------|
| **Domain**       | E-Commerce / Retail                             |
| **Role Target**  | Requirements Analyst / Business Analyst         |
| **Dataset**      | 2,000 synthetic orders (Jan–Dec 2023)           |
| **Tools Used**   | Python, SQL (MySQL), Excel, Power BI            |
| **Libraries**    | Pandas, NumPy, Matplotlib, Seaborn, openpyxl   |

---

## Business Problem

An e-commerce company wants to understand:
- Which product categories and regions drive the most revenue?
- How does revenue trend month-over-month?
- What is the order delivery vs. return rate?
- Which payment methods do customers prefer?
- Who are the top customers, and what is the average order value?

---

## Project Structure

```
ecommerce_dashboard/
├── data/
│   └── ecommerce_sales.csv       # 2,000 order records
├── sql/
│   └── kpi_queries.sql           # 10 business KPI queries
├── outputs/
│   ├── chart1_monthly_revenue.png
│   ├── chart2_category_revenue.png
│   ├── chart3_regional_revenue.png
│   ├── chart4_top_products.png
│   ├── chart5_order_status.png
│   ├── chart6_payment_methods.png
│   └── ecommerce_report.xlsx     # Multi-sheet Excel report
├── generate_data.py              # Synthetic dataset generator
├── eda_analysis.py               # EDA + 6 chart visualizations
├── excel_report.py               # Automated Excel report
├── powerbi_guide.txt             # Power BI step-by-step setup
└── README.md
```

---

## Key Business Insights

- **Electronics** is the highest revenue category (~35% of total)
- **North region** leads in sales, followed by South
- **78% delivery rate** with 10% returns — scope for logistics improvement
- **UPI & Credit Card** are the most preferred payment methods
- Revenue peaks in **Q4** — seasonal demand pattern
- Customers aged **26–35** are the highest-spending segment

---

## How to Run

### 1. Clone the repository
```bash
git clone https://github.com/senthil203/ecommerce-sales-dashboard.git
cd ecommerce-sales-dashboard
```

### 2. Install dependencies
```bash
pip install pandas numpy matplotlib seaborn openpyxl
```

### 3. Generate dataset
```bash
python generate_data.py
```

### 4. Run EDA and generate charts
```bash
python eda_analysis.py
```

### 5. Generate Excel report
```bash
python excel_report.py
```

### 6. SQL Analysis
- Open `sql/kpi_queries.sql` in MySQL Workbench
- Import `data/ecommerce_sales.csv` into the `ecommerce_db` database
- Run each query to extract KPIs

### 7. Power BI Dashboard
- Follow the step-by-step guide in `powerbi_guide.txt`
- Import `data/ecommerce_sales.csv` into Power BI Desktop

---

## Visualizations

| Chart | Description |
|-------|-------------|
| Monthly Revenue Trend | Line chart of delivered revenue Jan–Dec 2023 |
| Category Revenue | Horizontal bar comparing 5 product categories |
| Regional Distribution | Donut chart of 5 regional revenue shares |
| Top 10 Products | Bar chart of highest-earning products |
| Order Status by Quarter | Stacked bar of delivery/return/cancel rates |
| Payment Methods | Bar chart of order count by payment type |

---

## Skills Demonstrated

- **Data Analysis** — EDA, KPI identification, trend analysis
- **SQL** — Aggregations, window functions, CASE statements, subqueries
- **Python** — Pandas for data wrangling, Matplotlib/Seaborn for visualization
- **Excel** — Multi-sheet reporting, conditional formatting, pivot-ready structure
- **Power BI** — DAX measures, interactive dashboard, slicer filters
- **Business Thinking** — Translating raw data into stakeholder-ready insights

---

## Author

**Senthilkumar R**
MSc Data Science & Business Analytics — VISTAS, Chennai
[LinkedIn](https://www.linkedin.com/in/ravi-senthil-369a03259) | [GitHub](https://github.com/senthil203)
